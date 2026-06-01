<!--
@component
Displays the current solve time and hint text, driven by an internal inspection/solve state machine.

State machine transitions:
  waiting → inspection → running → stopped
  inspection or running → waiting  (Escape cancel; fires onTimerCancel)
  inspection expires past -2s → dnf  (acknowledging fires onTimerComplete with dnf=true)

TODO: clean up state transition description above once kinks are ironed out
-->

<script lang="ts">
  import { onDestroy } from 'svelte';
  import { getHintText, getMobileHintText, type TimerMode } from './timerUtils.js';

  interface Props {
    onDnf?: () => void;
    onTimerCancel?: () => void;
    onTimerComplete?: (timeMs: number, inspectionPenalty: boolean, dnf: boolean) => void;
  }

  const { onDnf, onTimerComplete, onTimerCancel }: Props = $props();

  const INSPECTION_TIME_TOTAL = 15;

  // ------------------------
  // ---- Reactive state ----
  // ------------------------

  // The elapsed time (while timer is running) and final time (once stopped)
  let finalMillis = $state(0);
  let elapsedMillis = $state(0);

  // Whether the current solve is a DNF, or had inspection penalty
  let isDnf = $state(false);
  let isInspectionPenalty = $state(false);

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
        return formatMs(elapsedMillis);
      case 'stopped':
        return formatMs(finalMillis);
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
   * Format a millisecond value as seconds with 2 decimals,
   * or if greater than 1 minute, as minutes + seconds with 2 decimals.
   */
  function formatMs(ms: number): string {
    const totalSecs = Math.floor(ms / 1000);
    const centis = Math.floor((ms % 1000) / 10);
    if (totalSecs < 60) {
      return `${totalSecs}.${centis.toString().padStart(2, '0')}`;
    }
    const mins = Math.floor(totalSecs / 60);
    const secs = totalSecs % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}.${centis.toString().padStart(2, '0')}`;
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
    isInspectionPenalty = false;
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
    isInspectionPenalty = false;

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
    isInspectionPenalty = remainingInspectionTimeSeconds < 0;

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

    // Calculate the final elapsed time for this solve, and then execute the callback function
    // to either record the solve for this week's competition if currently competing, or save
    // the solve to their practice session if practicing.
    finalMillis = Date.now() - runStartTime;
    onTimerComplete?.(finalMillis, isInspectionPenalty, false);
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
    // session if practicing.
    isDnf = true;
    onDnf?.();
  }

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

    // Any key stops the running timer to complete the solve.
    if (timerState === 'running') {
      transitionToStopped();
      return;
    }

    // Pressing *down* space will "arm" the timer (spaceHeld=true) to transition to a running
    // timer from waiting/inspection/stopped.
    if (e.key === ' ') {
      e.preventDefault();
      if (timerState === 'waiting' || timerState === 'inspection' || timerState === 'stopped') {
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
    } else if (timerState === 'stopped') {
      transitionToWaiting();
    }
  }

  function handleTouchStart(e: TouchEvent) {
    e.preventDefault();
    spaceHeld = true;
  }

  function handleTouchEnd(e: TouchEvent) {
    e.preventDefault();
    spaceHeld = false;

    if (timerState === 'dnf') {
      const wasDnf = isDnf;
      transitionToWaiting();
      onTimerComplete?.(0, false, wasDnf);
      return;
    }
    if (timerState === 'waiting') transitionToInspection();
    else if (timerState === 'running') transitionToStopped();
    else if (timerState === 'stopped') transitionToWaiting();
    else if (timerState === 'inspection') transitionToRunning();
  }

  // Signals to the navbar and event selector (via CSS) that they should be locked while
  // the timer is active. Body class is used because those elements are outside this
  // component's subtree and don't share a common parent that could hold this state.
  $effect(() => {
    document.body.classList.toggle(
      'timer-active',
      timerState === 'inspection' || timerState === 'running'
    );
    return () => document.body.classList.remove('timer-active');
  });

  onDestroy(clearIntervals);
</script>

<svelte:window onkeydown={handleKeydown} onkeyup={handleKeyUp} />

<!--
  Nearly full-screen overlay on mobile during inspection and running; covers all other UI so
  the user has a large tap target for their timer interactions.
-->
<div
  class="mobile-overlay"
  class:active={timerState === 'inspection' || timerState === 'running'}
  ontouchstart={handleTouchStart}
  ontouchend={handleTouchEnd}
></div>

<div
  class="timer-area"
  class:elevated={timerState === 'inspection' || timerState === 'running'}
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
