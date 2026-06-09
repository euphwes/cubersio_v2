<!--
@component
Main panel for the compete view. Contains the scramble bar, solve timer, post-solve actions
(DNF/+2 penalty toggles, submit, discard), and a results area showing the user's solves in
the active event. Once the event is complete, the scramble bar is hidden and a summary
display replaces the timer.
-->

<script lang="ts">
  import { getContext } from 'svelte';
  import { formatSolve } from '$lib/formatSolve.js';
  import type { EventSlug } from '$lib/types.js';
  import type { CompetitionStore } from '$lib/competition.svelte.js';
  import type { NavigationLock } from '$lib/navigationLock.svelte.js';
  import Timer from './Timer.svelte';
  import EventImage from './EventImage.svelte';
  import EventCompleteBanner from './EventCompleteBanner.svelte';
  import EventResultsCard from './EventResultsCard.svelte';

  interface Props {
    selectedEventSlug: EventSlug;
  }

  const { selectedEventSlug }: Props = $props();

  const competitionContext = getContext<CompetitionStore>('competition');
  const navigationLock = getContext<NavigationLock>('navigationLock');

  // TODO runtime validation that we actually have scrambles for every event
  const eventScrambles = $derived(competitionContext.scrambles[selectedEventSlug] ?? []);
  // TODO runtime validation that we actually have a participation record for every event,
  // so downstream stuff doesn't have to null-coalesce (participation?.solves, etc)
  const participation = $derived(competitionContext.userParticipation[selectedEventSlug]);

  const eventInfo = $derived(competitionContext.events[selectedEventSlug]);
  const eventFormat = $derived(eventInfo.format);

  // Derive the current scramble based on how many solves the user has recorded for this event.
  const solveCount = $derived(participation?.solves.length ?? 0);
  const scramble = $derived(eventScrambles[solveCount] ?? '');

  // Once all solves are recorded, the scramble bar is hidden and the timer is replaced by
  // a text-based summary of the user's participation in this event.
  const eventIsComplete = $derived(participation?.status === 'complete');

  // Whether a completed solve is awaiting submit/discard. The solve itself (final time and
  // penalty flags) lives in the Timer and is read/written via its exported `solve` accessor.
  let showSolveSubmissionControls = $state(false);
  let timer = $state<Timer>();

  // Display for the pending solve on the submit button, reflecting any penalties
  const solveTimeOnSumbitButton = $derived.by(() => {
    if (!timer || !showSolveSubmissionControls) return '';
    return formatSolve({
      timeMs: timer.solve.timeMs,
      dnf: timer.solve.dnf,
      plusTwo: timer.solve.plusTwo,
      omittedFromAverage: false,
      pbSingle: false
    });
  });

  // When the DNF came from overflowing inspection, the penalty is not optional; the DNF and
  // +2 toggles are disabled and the user can only submit or discard.
  const penaltyTogglesLocked = $derived(timer?.solve.dnfViaInspection ?? false);

  function showSubmitControls() {
    showSolveSubmissionControls = true;
  }

  function hideSubmitControls() {
    showSolveSubmissionControls = false;
  }

  function toggleDnf() {
    if (timer) timer.solve.dnf = !timer.solve.dnf;
  }

  function togglePlusTwo() {
    if (timer) timer.solve.plusTwo = !timer.solve.plusTwo;
  }

  async function handleSubmit() {
    if (!timer || !showSolveSubmissionControls) return;
    const { timeMs, dnf, plusTwo } = timer.solve;
    await competitionContext.submitSolve(selectedEventSlug, {
      dnf,
      timeMs,
      plusTwo
    });
    showSolveSubmissionControls = false;
    // The final solve of an event unmounts the Timer (summary banner replaces it), which can
    // clear the binding during the await above; skip the reset in that case
    timer?.reset();
  }

  function handleDiscard() {
    showSolveSubmissionControls = false;
    timer?.reset();
  }

  // Keep navigation locked while a completed solve is awaiting submit/discard; otherwise the
  // user could switch events and the pending solve would be submitted against the wrong event.
  // The cleanup clears the flag so the lock can't outlive this panel.
  $effect(() => {
    navigationLock.solvePending = showSolveSubmissionControls;
    return () => {
      navigationLock.solvePending = false;
    };
  });
</script>

<!-- Timer zone -->
<div class="compete-panel">
  <div class="timer-zone">
    <!-- Scramble bar (hidden once the event is complete) -->
    {#if !eventIsComplete}
      <div class="scramble-bar">
        <p class="scramble-text">{scramble}</p>
        <div class="scramble-bar-preview">
          <EventImage eventSlug={selectedEventSlug} solved={false} />
        </div>
      </div>
    {/if}

    <!-- Timer, replaced by the event summary once the event is complete -->
    <div class="timer-wrapper">
      {#if eventIsComplete && participation}
        <EventCompleteBanner eventName={eventInfo.name} {eventFormat} result={participation} />
      {:else}
        <Timer
          bind:this={timer}
          onTimerComplete={showSubmitControls}
          onTimerCancel={hideSubmitControls}
          onDnf={showSubmitControls}
        />
      {/if}
    </div>

    <!-- Action buttons -->
    <div class="timer-actions">
      {#if showSolveSubmissionControls}
        <button
          class="btn-action btn-toggle"
          class:active={timer?.solve.plusTwo}
          aria-pressed={timer?.solve.plusTwo ?? false}
          disabled={penaltyTogglesLocked}
          onclick={togglePlusTwo}
        >
          +2
        </button>
        <button
          class="btn-action btn-toggle"
          class:active={timer?.solve.dnf}
          aria-pressed={timer?.solve.dnf ?? false}
          disabled={penaltyTogglesLocked}
          onclick={toggleDnf}
        >
          DNF
        </button>
        <button class="btn-action btn-submit" onclick={handleSubmit}>
          Submit {solveTimeOnSumbitButton}
        </button>
        <button class="btn-action btn-discard" onclick={handleDiscard}>Discard</button>
      {/if}
    </div>
  </div>

  <!-- Bottom zone: my-solves results + scramble preview -->
  <div class="bottom-zone">
    <EventResultsCard {participation} {eventInfo} />

    <!-- Scramble preview image (desktop only) -->
    <div class="scramble-preview">
      <div class="scramble-preview-image">
        <EventImage eventSlug={selectedEventSlug} solved={false} />
      </div>
    </div>
  </div>
</div>

<style>
  /* --------------------------------------------- */
  /* ----------- Mobile-first defaults ----------- */
  /* --------------------------------------------- */

  /* Local color tokens for values not yet in the global design system */
  .compete-panel {
    --color-danger: #e53e3e;

    position: relative;
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 100%;
    overflow: hidden;
    color: var(--text-primary);
  }

  /* ----- Timer zone ----- */

  .timer-zone {
    flex: 1;
    display: flex;
    flex-direction: column;
    padding: 0.75rem 1rem 0.625rem;
    gap: 0.5rem;
    border-bottom: 1px solid color-mix(in srgb, var(--text-primary) 10%, transparent);
    overflow: hidden;
    min-height: 0;
  }

  .scramble-bar {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    background: var(--surface-card);
    border: 1px solid color-mix(in srgb, var(--text-primary) 12%, transparent);
    border-radius: 0.375rem;
    padding: 0.5rem 0.625rem 0.5rem 0.875rem;
    flex-shrink: 0;
  }

  .scramble-text {
    flex: 1;
    margin: 0;
    font-family: monospace;
    font-size: 1.25rem;
    line-height: 1.5;
    color: var(--text-primary);
    word-break: break-word;
    text-align: left;
  }

  /* Shown on mobile alongside the scramble text */
  .scramble-bar-preview {
    display: block;
    width: 48px;
    height: 48px;
    flex-shrink: 0;
  }

  .timer-wrapper {
    flex: 1;
    display: flex;
    flex-direction: column;
    min-height: 0;
    /* Scales the timer display within this panel */
    --timer-font-size: 24vw;
  }

  .timer-actions {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    flex-shrink: 0;
  }

  .btn-action {
    padding: 0.375rem 1rem;
    border-radius: 0.375rem;
    font-size: 0.8rem;
    font-weight: 600;
    cursor: pointer;
    transition:
      background 0.15s ease,
      border-color 0.15s ease,
      color 0.15s ease;
  }

  .btn-toggle {
    background: transparent;
    border: 1px solid color-mix(in srgb, var(--text-primary) 20%, transparent);
    color: var(--text-muted);
  }

  .btn-toggle:hover:not(:disabled) {
    border-color: color-mix(in srgb, var(--text-primary) 40%, transparent);
    color: var(--text-primary);
  }

  .btn-toggle.active {
    background: color-mix(in srgb, var(--color-danger) 12%, transparent);
    border-color: var(--color-danger);
    color: var(--color-danger);
  }

  .btn-toggle:disabled {
    opacity: 0.55;
    cursor: not-allowed;
  }

  .btn-submit {
    background: var(--brand);
    border: 1px solid var(--brand);
    color: #fff;
  }

  .btn-submit:hover {
    background: color-mix(in srgb, var(--brand) 82%, black);
  }

  .btn-discard {
    background: transparent;
    border: 1px solid color-mix(in srgb, var(--color-danger) 55%, transparent);
    color: var(--color-danger);
  }

  .btn-discard:hover {
    background: color-mix(in srgb, var(--color-danger) 8%, transparent);
  }

  /* ----- Bottom zone ----- */

  .bottom-zone {
    flex: 0 0 auto;
    height: 36vh;
    display: flex;
    flex-direction: row;
    gap: 0.75rem;
    padding: 0.75rem;
    overflow: hidden;
    min-height: 0;
  }

  /* Hidden on mobile; desktop shows it alongside the results table */
  .scramble-preview {
    display: none;
  }

  /* --------------------------------------------- */
  /* ---------- Desktop style overrides ---------- */
  /* --------------------------------------------- */

  @media (min-width: 768px) {
    .timer-zone {
      flex: 0 0 66%;
      padding: 1rem 1.5rem 0.75rem;
      gap: 0.75rem;
    }

    .scramble-text {
      font-size: 1.5rem;
      text-align: center;
    }

    /* On desktop the scramble preview moves to its own panel in the bottom zone */
    .scramble-bar-preview {
      display: none;
    }

    .timer-wrapper {
      min-height: 0;
      --timer-font-size: 12vw;
    }

    .bottom-zone {
      flex: 1;
      height: auto;
    }

    .scramble-preview {
      flex: 1;
      display: flex;
      align-items: center;
      justify-content: center;
      background: var(--surface-card);
      border-radius: 0.375rem;
      border: 1px solid color-mix(in srgb, var(--text-primary) 8%, transparent);
    }

    .scramble-preview-image {
      width: 180px;
      height: 180px;
    }
  }
</style>
