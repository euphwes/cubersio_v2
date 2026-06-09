<!--
@component
Displays the current solve time and hint text, driven by an internal inspection/solve state
machine.

Owns the solve's state (final time, DNF and +2 penalty flags); parents can read a complete solve
through the export `solve` accessor.
-->

<script lang="ts">
  import { getContext, onDestroy } from 'svelte';
  import { formatSolve } from '$lib/formatSolve.js';
  import type { NavigationLock } from '$lib/navigationLock.svelte.js';

  interface Props {
    onDnf?: () => void;
    onTimerCancel?: () => void;
    onTimerComplete?: () => void;
  }

  const { onDnf, onTimerComplete, onTimerCancel }: Props = $props();

  const navigationLock = getContext<NavigationLock>('navigationLock');

  const INSPECTION_TIME_TOTAL = 15;

  type TimerMode = 'waiting' | 'inspection' | 'running' | 'stopped' | 'dnf';

  function getHintText(mode: TimerMode): string {
    switch (mode) {
      case 'waiting':
        return 'Press Space to begin inspection';
      case 'inspection':
        return 'Press Space to start - Esc to cancel';
      case 'running':
        return 'Press any key to stop';

      // No hint for the DNF or stopped states; the Timer component consumers handle behavior.
      case 'dnf':
        return '';
      case 'stopped':
        return '';
    }
  }

  function getMobileHintText(mode: TimerMode): string {
    switch (mode) {
      case 'waiting':
        return 'Tap to begin inspection';
      case 'inspection':
        return 'Tap to start timer';
      case 'running':
        return 'Tap to stop';

      // No hint for the DNF or stopped states; the Timer component consumers handle behavior.
      case 'dnf':
        return '';
      case 'stopped':
        return '';
    }
  }

  // ------------------------
  // ---- Reactive state ----
  // ------------------------

  // The elapsed time (while timer is running) and final time (once stopped)
  let finalMillis = $state(0);
  let elapsedMillis = $state(0);

  // Penalty flags for the current solve. The +2 flag is set automatically when inspection
  // runs past 15 seconds; both flags can also be toggled by the parent via the exported
  // `solve` accessor after a solve completes.
  let isDnf = $state(false);
  let isPlusTwo = $state(false);

  // Set when the solve becomes DNF by overflowing inspection time. In that case the penalty
  // flags are locked (the DNF is not optional), so the user can only submit or discard.
  let dnfViaInspection = $state(false);

  // The currently-remaining number of seconds on the inspection timer, used to drive the
  // visual inspection time countdown.
  let remainingInspectionTimeSeconds = $state(INSPECTION_TIME_TOTAL);

  // Internal state of the timer, such as the current mode (waiting, inspection time, running),
  // and whether the space bar is currently being held down to arm a timer transition
  let spaceHeld = $state(false);
  let timerState = $state<TimerMode>('waiting');

  // The timer is "armed" when space is held during waiting or inspection, which means it's
  // ready to change states from waiting → inspection, or inspection → running
  const isArmed = $derived(spaceHeld && (timerState === 'waiting' || timerState === 'inspection'));

  // The value actually displayed in the timer text: either the current inspection countdown
  // value, or the running timer value, or the final result.
  const displayTime = $derived.by(() => {
    switch (timerState) {
      case 'waiting':
        return '0.00';
      case 'inspection':
        return String(remainingInspectionTimeSeconds);
      case 'dnf':
        return 'DNF';
      case 'running':
        return formatSolve({
          timeMs: elapsedMillis,
          // Penalties aren't shown while the solve is still in progress
          dnf: false,
          plusTwo: false,
          // Irrelevant here, the solve is still in-progress
          omittedFromAverage: false,
          pbSingle: false
        });
      case 'stopped':
        return formatSolve({
          timeMs: finalMillis,
          // Reflects the penalty flags so the display matches the pending solve's notation
          dnf: isDnf,
          plusTwo: isPlusTwo,
          omittedFromAverage: false,
          pbSingle: false
        });
    }
  });

  const decimalIdx = $derived(displayTime.indexOf('.'));

  // The usage hints display under the timer display value, to indicate to the user how to
  // interact with the timer
  const hintText = $derived(getHintText(timerState));
  const mobileHintText = $derived(getMobileHintText(timerState));

  // -------------------------
  // -- Non-state variables --
  // -------------------------

  // Store the time that the timer started (when running), or the countdown started, so we can
  // calculate elapsed time or time remaining on the countdown to display
  let runStartTime = 0;
  let inspectionStartTime = 0;

  // Store the IDs of the periodic intervals running to recalculate and update the running
  // timer or countdown display values, so we can cancel those timers when changing timer state.
  let runningIntervalId: ReturnType<typeof setInterval> | null = null;
  let inspectionIntervalId: ReturnType<typeof setInterval> | null = null;

  // ---------------------------
  // ---- Utility functions ----
  // ---------------------------

  function clearIntervals() {
    if (runningIntervalId !== null) {
      clearInterval(runningIntervalId);
      runningIntervalId = null;
    }
    if (inspectionIntervalId !== null) {
      clearInterval(inspectionIntervalId);
      inspectionIntervalId = null;
    }
  }

  function calculateRemainingInspectionTime() {
    remainingInspectionTimeSeconds =
      INSPECTION_TIME_TOTAL - Math.floor((Date.now() - inspectionStartTime) / 1000);

    if (remainingInspectionTimeSeconds < -2) {
      transitionToDnf();
    }
  }

  function calculateElapsedTime() {
    elapsedMillis = Date.now() - runStartTime;
  }

  /**
   * Drops focus from whatever element currently has it (e.g. an event card the user just
   * clicked in the sidebar). Called when the timer captures a keypress, so the focused
   * element doesn't also react to it (a focused button activates on Space).
   */
  function blurFocusedElement() {
    if (document.activeElement instanceof HTMLElement) {
      document.activeElement.blur();
    }
  }

  // --------------------------------
  // -- State transition functions --
  // --------------------------------

  /**
   * Transition to the "waiting" state.
   *
   * This is the default state where no timer activity is happening. From here, the user can
   * press the spacebar or tap their screen to begin inspection time.
   */
  function transitionToWaiting() {
    clearIntervals();

    timerState = 'waiting';
    spaceHeld = false;

    finalMillis = 0;
    elapsedMillis = 0;
    remainingInspectionTimeSeconds = INSPECTION_TIME_TOTAL;

    isDnf = false;
    isPlusTwo = false;
    dnfViaInspection = false;
  }

  /**
   * Transition to the "inspection" state.
   *
   * In this state, a 15-second inspection time display is counting down. The user has to
   * press and hold space or tap the screen again to start the timer running.
   */
  function transitionToInspection() {
    clearIntervals();

    timerState = 'inspection';

    // Clear any penalties from a previous solve.
    isDnf = false;
    isPlusTwo = false;
    dnfViaInspection = false;

    // Reset the remaining inspection time back to the base amount
    remainingInspectionTimeSeconds = INSPECTION_TIME_TOTAL;

    // Record when inspection started, and kick off an interval that periodically calculates
    // the remaining inspection time and sets a reactive state variable which drives the timer
    // display value.
    inspectionStartTime = Date.now();
    inspectionIntervalId = setInterval(calculateRemainingInspectionTime, 50);
  }

  /**
   * Transition to the "running" state.
   *
   * The user is in the middle of a solve, and the timer is actively running to display the
   * elapsed time.
   */
  function transitionToRunning() {
    clearIntervals();

    timerState = 'running';

    // There's an inspection time penalty (+2 seconds) if the user exceeds 15 seconds during
    // their inspection before starting the timer.
    isPlusTwo = remainingInspectionTimeSeconds < 0;

    // Clear the elapsed time from any previous solves, and record the time this current solve
    // started. Kick off an interval that periodically calculates the elapsed time for the
    // active solve, setting a reactive state variable which drives the timer display value.
    elapsedMillis = 0;
    runStartTime = Date.now();
    runningIntervalId = setInterval(calculateElapsedTime, 41);
  }

  /**
   * Transition to the "stopped" state.
   *
   * The user has completed their solve.
   */
  function transitionToStopped() {
    clearIntervals();

    timerState = 'stopped';

    // Calculate the final elapsed time for this solve, then notify the parent. The parent
    // reads the solve details (time and penalty flags) through the `solve` accessor.
    finalMillis = Date.now() - runStartTime;
    onTimerComplete?.();
  }

  /**
   * Transition to the "DNF" (did not finish) state.
   *
   * The user exceeded their 15 seconds of inspection time, and 2 additional seconds where
   * inspection penalty would have applied but they could complete their solve, and now the
   * solve is considered DNF.
   */
  function transitionToDnf() {
    clearIntervals();

    timerState = 'dnf';

    // Set the DNF flag and then execute the callback function to either record the solve for
    // this week's competition if currently competing, or save the solve to their practice
    // session if practicing. This DNF came from overflowing inspection, so the penalty flags
    // are locked; the solve can only be submitted as DNF or discarded.
    isDnf = true;
    dnfViaInspection = true;
    onDnf?.();
  }

  /**
   * Resets the timer back to the waiting state (0.00). Exposed so the parent can clear the
   * displayed result, e.g. when the user discards a pending solve.
   */
  export function reset() {
    transitionToWaiting();
  }

  /**
   * Read/write access to the current solve's state. Parents pull the final time and penalty
   * flags from here when a solve completes, and may toggle the penalty flags before the solve
   * is recorded. DNF and +2 are mutually exclusive; setting one clears the other. When the
   * DNF came from overflowing inspection (`dnfViaInspection`), the penalty flags are locked
   * and the setters ignore writes.
   */
  export const solve = {
    get timeMs() {
      return finalMillis;
    },
    get dnfViaInspection() {
      return dnfViaInspection;
    },
    get dnf() {
      return isDnf;
    },
    set dnf(value: boolean) {
      if (dnfViaInspection) return;
      isDnf = value;
      if (value) isPlusTwo = false;
    },
    get plusTwo() {
      return isPlusTwo;
    },
    set plusTwo(value: boolean) {
      if (dnfViaInspection) return;
      isPlusTwo = value;
      if (value) isDnf = false;
    }
  };

  function handleKeydown(e: KeyboardEvent) {
    if (e.repeat) return;

    // Pressing Esc will cancel a running timer, or an inspection time countdown.
    if (e.key === 'Escape') {
      if (timerState === 'running' || timerState === 'inspection') {
        transitionToWaiting();
        onTimerCancel?.();
      }
      return;
    }

    // Any key stops the running timer to complete the solve. Blurring first means the
    // keyup won't activate a still-focused element elsewhere on the page. Space also
    // needs its default suppressed, or it scrolls the page or a focused scroll
    // container (e.g. the event card list) after stopping the timer.
    if (timerState === 'running') {
      if (e.key === ' ') {
        e.preventDefault();
      }
      blurFocusedElement();
      transitionToStopped();
      return;
    }

    // Pressing *down* space will "arm" the timer (spaceHeld=true) to transition from
    // waiting to inspection, or from inspection to running. The stopped state ignores
    // space: the pending solve is resolved through the submit/discard controls, and the
    // parent resets the timer afterward.
    if (e.key === ' ') {
      e.preventDefault();
      if (timerState === 'waiting' || timerState === 'inspection') {
        blurFocusedElement();
        spaceHeld = true;
      }
    }
  }

  function handleKeyUp(e: KeyboardEvent) {
    if (e.key !== ' ' || !spaceHeld) return;

    spaceHeld = false;

    if (timerState === 'waiting') {
      transitionToInspection();
    } else if (timerState === 'inspection') {
      transitionToRunning();
    }
  }

  function handleTouchStart(e: TouchEvent) {
    e.preventDefault();
    spaceHeld = true;
  }

  function handleTouchEnd(e: TouchEvent) {
    e.preventDefault();
    spaceHeld = false;

    // Like space on desktop, taps are ignored in the stopped and dnf states; the pending
    // solve keeps its time and penalty flags until it's resolved through the submit/discard
    // controls, after which the parent resets the timer
    if (timerState === 'waiting') transitionToInspection();
    else if (timerState === 'running') transitionToStopped();
    else if (timerState === 'inspection') transitionToRunning();
  }

  // Lock navigation (navbar and event sidebar) while the timer is active. The lock lives in
  // a shared context because those elements are outside this component's subtree. The cleanup
  // clears the flag so the lock can't outlive an unmounted timer.
  $effect(() => {
    navigationLock.timerActive = timerState === 'inspection' || timerState === 'running';
    return () => {
      navigationLock.timerActive = false;
    };
  });

  onDestroy(clearIntervals);
</script>

<svelte:window onkeydown={handleKeydown} onkeyup={handleKeyUp} />

<!--
  Nearly full-screen overlay on mobile during inspection and running; covers all other UI so
  the user has a large tap target for their timer interactions.
-->
<!--
  Both touch surfaces are role="button" with tabindex="-1": they act as buttons for touch
  users, but stay out of the tab order because keyboard users interact with the timer
  through the window-level Space/Escape handlers instead.
-->
<div
  class="mobile-overlay"
  class:active={timerState === 'inspection' || timerState === 'running'}
  role="button"
  tabindex="-1"
  aria-label="Timer touch area"
  ontouchstart={handleTouchStart}
  ontouchend={handleTouchEnd}
></div>

<div
  class="timer-area"
  class:elevated={timerState === 'inspection' || timerState === 'running'}
  role="button"
  tabindex="-1"
  ontouchstart={handleTouchStart}
  ontouchend={handleTouchEnd}
>
  <div class="timer-display" class:armed={isArmed}>
    {#if decimalIdx !== -1}
      {displayTime.slice(0, decimalIdx)}<span class="timer-decimal"
        >{displayTime.slice(decimalIdx)}</span
      >
    {:else}
      {displayTime}
    {/if}
  </div>
  <p class="timer-hint desktop-hint">{hintText}</p>
  <p class="timer-hint mobile-hint">{mobileHintText}</p>
</div>

<style>
  /* --------------------------------------------- */
  /* ----------- Mobile-first defaults ----------- */
  /* --------------------------------------------- */

  .mobile-overlay {
    display: none;
  }

  .mobile-overlay.active {
    display: block;
    position: absolute;
    inset: 0;
    z-index: 100;
    touch-action: none;
    background-color: var(--surface);
  }

  /* Float the timer display above the overlay so it's visible while the overlay
     covers everything else. */
  .timer-area.elevated {
    position: relative;
    z-index: 101;
  }

  .timer-area {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    min-height: 0;
    touch-action: none;
    user-select: none;
  }

  .timer-display {
    font-family: 'csTimer', monospace;
    font-size: var(--timer-font-size, 20vw);
    font-weight: 400;
    letter-spacing: 0.05em;
    line-height: 1;
    color: var(--text-primary);
    transition: color 0.1s ease;
  }

  .timer-display.armed {
    color: var(--brand);
  }

  .timer-decimal {
    font-size: 0.725em;
  }

  .timer-hint {
    margin: 0;
    font-size: 1rem;
    color: var(--text-muted);
    opacity: 0.6;
  }

  .desktop-hint {
    display: none;
  }

  /* --------------------------------------------- */
  /* ---------- Desktop style overrides ---------- */
  /* --------------------------------------------- */

  @media (min-width: 1024px) {
    .mobile-overlay.active {
      display: none;
    }

    .timer-display {
      font-size: var(--timer-font-size, 18vw);
    }

    .desktop-hint {
      display: block;
    }

    .mobile-hint {
      display: none;
    }
  }
</style>
