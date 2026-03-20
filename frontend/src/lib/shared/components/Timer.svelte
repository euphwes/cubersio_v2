<!--
@component
Solve timer state machine.

Modes:  waiting → countdown → running → stopped
Cancel: escape from countdown/running → waiting (fires onTimerCancel)
DNF:    countdown expires past -2s → dnf; acknowledging fires onTimerComplete(0, false, true)

Props:
  onTimerComplete(timeMs, inspectionPenalty, dnf) — fired when a solve completes or is DNF'd
  onTimerCancel — fired on explicit escape key cancel
-->

<script lang="ts">
  import { onDestroy } from 'svelte';

  const {
    onTimerComplete,
    onTimerCancel
  }: {
    onTimerComplete?: (timeMs: number, inspectionPenalty: boolean, dnf: boolean) => void;
    onTimerCancel?: () => void;
  } = $props();

  type TimerMode = 'waiting' | 'countdown' | 'dnf' | 'running' | 'stopped';

  let mode = $state<TimerMode>('waiting');
  let countdownValue = $state(15);
  let elapsedMs = $state(0);
  let finalMs = $state(0);
  let spaceHeld = $state(false);
  let isInspectionPenalty = $state(false);
  let isDnf = $state(false);

  let runningIntervalId: ReturnType<typeof setInterval> | null = null;
  let countdownIntervalId: ReturnType<typeof setInterval> | null = null;
  let runStartTime = 0;
  let countdownStartTime = 0;

  function clearIntervals() {
    if (runningIntervalId !== null) {
      clearInterval(runningIntervalId);
      runningIntervalId = null;
    }
    if (countdownIntervalId !== null) {
      clearInterval(countdownIntervalId);
      countdownIntervalId = null;
    }
  }

  function toWaiting() {
    clearIntervals();
    mode = 'waiting';
    countdownValue = 15;
    elapsedMs = 0;
    finalMs = 0;
    spaceHeld = false;
    isInspectionPenalty = false;
    isDnf = false;
  }

  function toCountdown() {
    clearIntervals();
    isInspectionPenalty = false;
    isDnf = false;
    countdownValue = 15;
    countdownStartTime = Date.now();
    mode = 'countdown';
    countdownIntervalId = setInterval(() => {
      countdownValue = 15 - Math.floor((Date.now() - countdownStartTime) / 1000);
      if (countdownValue < -2) {
        clearIntervals();
        isDnf = true;
        mode = 'dnf';
      }
    }, 50);
  }

  function toRunning() {
    clearIntervals();
    isInspectionPenalty = countdownValue < 0;
    runStartTime = Date.now();
    elapsedMs = 0;
    mode = 'running';
    runningIntervalId = setInterval(() => {
      elapsedMs = Date.now() - runStartTime;
    }, 41);
  }

  function toStopped() {
    finalMs = Date.now() - runStartTime;
    clearIntervals();
    mode = 'stopped';
    onTimerComplete?.(finalMs, isInspectionPenalty, false);
  }

  function handleKeydown(e: KeyboardEvent) {
    if (e.repeat) return;

    // DNF acknowledgement — treat as a completed attempt, fire onTimerComplete
    if (mode === 'dnf') {
      const wasDnf = isDnf;
      toWaiting();
      onTimerComplete?.(0, false, wasDnf);
      return;
    }

    if (e.key === 'Escape') {
      if (mode === 'running' || mode === 'countdown') {
        toWaiting();
        onTimerCancel?.();
      }
      return;
    }

    // Any key (including space) stops the running timer
    if (mode === 'running') {
      toStopped();
      return;
    }

    if (e.key === ' ') {
      e.preventDefault();
      if (mode === 'waiting' || mode === 'countdown' || mode === 'stopped') {
        spaceHeld = true;
      }
    }
  }

  function handleKeyup(e: KeyboardEvent) {
    if (e.key !== ' ' || !spaceHeld) return;
    spaceHeld = false;

    if (mode === 'waiting') {
      toCountdown();
    } else if (mode === 'countdown') {
      toRunning();
    } else if (mode === 'stopped') {
      toWaiting();
    }
  }

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

  const displayTime = $derived.by(() => {
    switch (mode) {
      case 'waiting':
        return '0.00';
      case 'countdown':
        return String(countdownValue);
      case 'dnf':
        return 'DNF';
      case 'running':
        return formatMs(elapsedMs);
      case 'stopped':
        return formatMs(finalMs);
    }
  });

  const hintText = $derived.by(() => {
    switch (mode) {
      case 'waiting':
        return 'Press Space to begin inspection';
      case 'countdown':
        return 'Press Space to start — Esc to cancel';
      case 'dnf':
        return 'DNF — press any key to record';
      case 'running':
        return 'Press any key to stop';
      case 'stopped':
        return 'Press Space for next solve';
    }
  });

  // Armed = space held during waiting or countdown → muted grey; otherwise black
  const isArmed = $derived(spaceHeld && (mode === 'waiting' || mode === 'countdown'));
  const decimalIdx = $derived(displayTime.indexOf('.'));

  onDestroy(clearIntervals);
</script>

<svelte:window onkeydown={handleKeydown} onkeyup={handleKeyup} />

<div class="timer-area">
  <div class="timer-display" class:armed={isArmed}>
    {#if decimalIdx !== -1}
      {displayTime.slice(0, decimalIdx)}<span class="timer-decimal"
        >{displayTime.slice(decimalIdx)}</span
      >
    {:else}
      {displayTime}
    {/if}
  </div>
  <p class="timer-hint">{hintText}</p>
</div>

<style>
  .timer-area {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    min-height: 0;
  }

  .timer-display {
    font-family: 'csTimer', monospace;
    font-size: 18vw;
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

  @media (max-width: 767px) {
    .timer-display {
      font-size: 20vw;
    }
  }
</style>
