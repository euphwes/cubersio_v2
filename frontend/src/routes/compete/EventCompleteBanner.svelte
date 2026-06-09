<!--
@component
Shown in place of the timer once the user has submitted all solves for an event.
Displays a congratulatory message acknowleding any PBs if they happened, or a
consolation message if the event finished with a DNF result. A large PB stamp is
anchored to the top-right of the container when any PB (single or result) was set.
-->

<script lang="ts">
  import type { EventFormat, EventParticipationRecord } from './types.js';
  import { hashObject } from '$lib/utils.js';
  import PbStamp from './PbStamp.svelte';

  interface Props {
    eventName: string;
    eventFormat: EventFormat;
    result: EventParticipationRecord;
  }

  const { eventName, eventFormat, result }: Props = $props();

  const EXCLAMATIONS = [
    'Amazing!',
    'Awesome!',
    'Brilliant.',
    'Clutch!',
    'Congrats!',
    'Crazy!',
    'Dude!',
    'Dope.',
    'Epic!',
    'Fire!',
    'Heck yeah!',
    'Huge!',
    'Incredible!',
    'Insane!',
    'Legendary.',
    "Let's go!",
    'Nice!',
    'Phenomenal!',
    'Sick.',
    'Superb!',
    'Sweet!',
    'Unreal!',
    'Wow.'
  ];

  const ENCOURAGEMENTS = [
    "Don't give up!",
    'Keep trying!',
    'Better luck next time!',
    'Never give up, never surrender!',
    'Hang in there.',
    'Stay strong.',
    'Believe in yourself.'
  ];

  const hasDnfResult = $derived(result.resultMs === null);
  const hasPbSingle = $derived(result.solves.some((s) => s.pbSingle));
  const hasPbResult = $derived(result.pbResult);
  const hasDualPb = $derived(hasPbSingle && hasPbResult);
  const hasAnyPb = $derived(hasPbSingle || hasPbResult);

  const resultIsAnAverage = $derived(eventFormat === 'ao5');
  const resultIsAMean = $derived(eventFormat === 'mo3');

  const summaryText = $derived.by(() => {
    if (hasDnfResult) {
      return `You finished ${eventName} with a DNF result.`;
    }
    if (hasDualPb) {
      if (resultIsAnAverage) {
        return `You finished ${eventName} with a PB single AND average!`;
      }
      if (resultIsAMean) {
        return `You finished ${eventName} with a PB single AND mean!`;
      }
    }
    if (hasPbResult) {
      if (resultIsAnAverage) {
        return `You finished ${eventName} with a PB average!`;
      }
      if (resultIsAMean) {
        return `You finished ${eventName} with a PB mean!`;
      }
    }
    if (hasPbSingle) {
      return `You finished ${eventName} with a PB single!`;
    }
    return `You finished ${eventName}!`;
  });

  // Pick an exclamation/encouragement by hashing the participation data.
  // This is deterministic for a given result, but varied across events and results.
  // hashObject's range is [0, n] inclusive, so n is the last index, the array length.
  const exclamation = $derived(EXCLAMATIONS[hashObject(result, EXCLAMATIONS.length - 1)]);
  const encouragement = $derived(ENCOURAGEMENTS[hashObject(result, ENCOURAGEMENTS.length - 1)]);
</script>

<div class="summary-display">
  {#if hasAnyPb}
    <div class="stamp-anchor">
      <PbStamp participation={result} />
    </div>
  {/if}
  {#if hasDnfResult}
    <p class="summary-text">{summaryText}</p>
    <p class="summary-text emphasis-text">{encouragement}</p>
  {:else}
    <p class="summary-text emphasis-text">{exclamation}</p>
    <p class="summary-text">{summaryText}</p>
  {/if}
</div>

<style>
  /* --------------------------------------------- */
  /* ----------- Mobile-first defaults ----------- */
  /* --------------------------------------------- */

  .summary-display {
    /* Positioning context for the top-right PB stamp overlay */
    position: relative;
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    min-height: 0;
  }

  .stamp-anchor {
    --pb-stamp-gap: 0;

    position: absolute;
    top: 1.25rem;
    right: 1.25rem;
    font-size: 3.5rem;
    line-height: 0;
  }

  .summary-text {
    margin: 0;
    font-size: 4.2vw;
    line-height: 1.3;
    color: var(--text-primary);
    text-align: center;
  }

  .emphasis-text {
    font-size: 4.5vw;
    font-weight: 700;
  }

  /* --------------------------------------------- */
  /* ---------- Desktop style overrides ---------- */
  /* --------------------------------------------- */

  @media (min-width: 1024px) {
    .stamp-anchor {
      top: 2rem;
      right: 2rem;
      font-size: 4.5rem;
    }

    .summary-text {
      font-size: 2vw;
    }

    .emphasis-text {
      font-size: 2.5vw;
    }
  }
</style>
