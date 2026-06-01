<!--
@component
A visual record of one event in the active competition

Displays the event name alongside the event image. Clicking the card switches to that event
in the competition timer panel, allowing the user to record their solves.
-->

<script lang="ts">
  import { nameByEventSlug } from './eventUtils.js';
  import type { EventSlug } from '$lib/types.js';
  import EventImage from './EventImage.svelte';

  interface EventCardProps {
    onclick: () => void;
    eventSlug: EventSlug;
    isSelected: boolean;
  }
  const { eventSlug, onclick, isSelected }: EventCardProps = $props();

  const eventName = $derived(nameByEventSlug[eventSlug] || eventSlug);
  const cardClass = $derived(isSelected ? 'event-card selected' : 'event-card');
</script>

<button class={cardClass} {onclick}>
  <div class="event-image-container">
    <div class="event-image">
      <!--
        .image-scaler sits between the fixed-size layout box (.event-image) and the SVG.
        Animating transform:scale() here instead of width/height on the outer box keeps
        the layout constant (no reflow) so the browser never re-rasterizes the SVG;
        it just scales an already-composited layer on the GPU.
      -->
      <div class="image-scaler">
        <EventImage {eventSlug} solved={false} />
      </div>
    </div>
  </div>
  <div class="event-info-container">
    <div class="event-title">{eventName}</div>
  </div>
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

  .event-image {
    width: 40px;
    height: 40px;
  }

  .image-scaler {
    width: 100%;
    height: 100%;
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
      background: #8b5cf6; /* vivid accent purple, intentionally brighter than --brand */
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
