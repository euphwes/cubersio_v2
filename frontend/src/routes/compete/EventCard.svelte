<!--
@component
A visual record of one event in the active competition

Displays the event name alongside the event image. Clicking the card switches to that event
in the competition timer panel, allowing the user to record their solves. Once the event is
complete, the image switches to its solved variant and the card shows the user's results.
-->

<script lang="ts">
  import { getContext } from 'svelte';
  import { formatBestSingle, formatEventResult } from '$lib/formatSolve.js';
  import { RESULT_LABEL_BY_FORMAT } from './eventUtils.js';
  import type { EventInfo } from './types.js';
  import type { CompetitionStore } from '$lib/competition.svelte.js';
  import EventImage from './EventImage.svelte';

  interface EventCardProps {
    onclick: () => void;
    event: EventInfo;
    isSelected: boolean;
  }
  const { event, onclick, isSelected }: EventCardProps = $props();

  const store = getContext<CompetitionStore>('competition');

  const cardClass = $derived(isSelected ? 'event-card selected' : 'event-card');

  const participation = $derived(store.userParticipation[event.slug]);
  const eventComplete = $derived(participation?.status === 'complete');

  // Once the event is complete, we show both the overall event result (mean, average),
  // and also the best single time. However, a "best of N" event's result IS the best single,
  // so the separate single row is omitted.
  const isBestOf = $derived(
    event.format === 'bo1' || event.format === 'bo3' || event.format === 'bo5'
  );

  const hasPbSingle = $derived(participation?.solves.some((s) => s.pbSingle) ?? false);

  const resultDisplay = $derived(formatEventResult(participation, { shouldAppendPb: false }));
  const singleDisplay = $derived(formatBestSingle(participation, { shouldAppendPb: false }));
</script>

<button class={cardClass} {onclick}>
  <div class="event-image-container">
    <div class="event-image">
      <!--
        .image-scaler sits between the fixed-size layout box (.event-image) and the SVG.
        Animating transform:scale() here instead of width/height on the outer box keeps
        the layout constant so the browser doesn't have to re-rasterizes the SVG, which
        can be expensive and degrade performance.
      -->
      <div class="image-scaler">
        <EventImage eventSlug={event.slug} solved={eventComplete} />
      </div>
    </div>
  </div>
  <div class="event-info-container">
    <div class="event-title">{event.name}</div>
  </div>
  {#if eventComplete && participation}
    <div class="event-results">
      <div class="result-row">
        <span class="result-label">{RESULT_LABEL_BY_FORMAT[event.format]}</span>
        <span class={['result-value', participation.pbResult && 'pb']}>{resultDisplay}</span>
      </div>
      {#if !isBestOf}
        <div class="result-row">
          <span class="result-label">single</span>
          <span class={['result-value', hasPbSingle && 'pb']}>{singleDisplay}</span>
        </div>
      {/if}
    </div>
  {/if}
</button>

<style>
  /* --------------------------------------------- */
  /* ----------- Mobile-first defaults ----------- */
  /* --------------------------------------------- */

  .event-card {
    cursor: pointer;
    display: flex;
    flex-direction: row;
    width: 100%;
    color: var(--text-primary);
    background-color: var(--surface-card);
    border: 1px solid var(--surface-card);
    border-radius: 0.25rem;
    transition: all 100ms ease;
  }

  .event-image-container {
    margin-left: 0.5rem;
    display: flex;
    align-items: center;
    padding: 0.375rem 0;
  }

  .event-info-container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 0.25rem;
    padding-left: 0.625rem;
    text-align: left;
  }

  .event-title {
    color: var(--text-primary);
    font-size: 0.875rem;
    font-weight: 500;
  }

  .event-results {
    margin-left: auto;
    /* Two shared columns (label, time) so the pieces of both rows align vertically;
       row wrappers use display: contents to place their children directly in this grid */
    display: grid;
    grid-template-columns: max-content max-content;
    align-content: center;
    align-items: center;
    column-gap: 0.5rem;
    row-gap: 0.4rem;
    padding: 0.375rem 0.75rem 0.375rem 0.5rem;
    font-size: 0.72rem;
    line-height: 1;
  }

  .result-row {
    display: contents;
  }

  .result-label {
    justify-self: end;
    font-size: 0.6rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--text-muted);
  }

  .result-value {
    justify-self: end;
    font-family: monospace;
    font-variant-numeric: tabular-nums;
    color: var(--text-primary);
  }

  .result-value.pb {
    font-weight: 700;
    text-shadow: 0 0 0.35em var(--pb-glow);
  }

  .event-image {
    width: 40px;
    height: 40px;
  }

  .image-scaler {
    width: 100%;
    height: 100%;
    filter: drop-shadow(0 6px 6px rgb(0 0 0 / 0.55));
  }

  /* --------------------------------------------- */
  /* ---------- Desktop style overrides ---------- */
  /* --------------------------------------------- */

  @media (min-width: 1024px) {
    .event-card {
      position: relative;
      border-radius: 0;
      border: none;
      border-bottom: 1px solid color-mix(in srgb, var(--text-primary) 8%, transparent);
      transition: background-color 0.1s ease;
    }

    .event-card::before {
      content: '';
      position: absolute;
      left: 4px;
      top: 4px;
      bottom: 4px;
      width: 4px;
      /* vivid accent purple, intentionally brighter than --brand */
      /* TODO give this a variable name in the app.css */
      background: #8b5cf6;
      border-radius: 2px;
      opacity: 0;
      transition: opacity 0.1s ease;
    }

    .event-card.selected {
      background-color: color-mix(in srgb, var(--brand) 14%, white);
    }

    .event-card.selected::before {
      opacity: 1;
    }

    .event-card:hover:not(.selected) {
      background-color: var(--surface-card-hover);
    }

    /* Layout box is always the selected (max) size - text position never shifts */
    .event-image {
      width: 68px;
      height: 68px;
    }

    /* Unselected: scale down to appear as ~48px (48/68 ≈ 0.706) */
    .image-scaler {
      transform: scale(0.706);
      transform-origin: center;
      transition: transform 0.15s ease;
      will-change: transform;
    }

    .event-card.selected .image-scaler {
      transform: scale(1);
    }

    .event-image-container {
      margin-left: 0.625rem;
      padding: 0.4rem 0;
    }

    .event-info-container {
      padding-left: 0.75rem;
      gap: 0.3rem;
    }
  }
</style>
