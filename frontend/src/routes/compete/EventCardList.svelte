<!--
@component
Scrollable list of event cards for the active competition.

On mobile: shows only the selected event card with a down-caret on the right.
Tapping it opens a full-screen overlay where the user can scroll and pick an event.

On desktop (>= 1024px): renders all events as a plain vertical scrollable list.
-->
<script lang="ts">
  import { fly } from 'svelte/transition';
  import { cubicOut } from 'svelte/easing';
  import EventCard from './EventCard.svelte';
  import type { EventSlug } from '$lib/types.js';
  import type { EventInfo } from './types.js';

  interface Props {
    events: EventInfo[];
    selectedEventSlug?: EventSlug;
    eventSelectionSetter: (slug: EventSlug) => void;
    competitionTitle?: string;
  }

  const {
    events,
    eventSelectionSetter,
    selectedEventSlug = '333',
    competitionTitle
  }: Props = $props();

  const selectedEvent = $derived(events.find((e) => e.slug === selectedEventSlug) ?? events[0]);

  let showEventPicker = $state(false);

  function selectEvent(slug: EventSlug) {
    eventSelectionSetter(slug);
    showEventPicker = false;
  }
</script>

<!-- Desktop: plain vertical list (hidden on mobile, replaced by picker) -->
<div class="event-list-wrapper">
  {#if competitionTitle}
    <p class="competition-label">{competitionTitle}</p>
  {/if}
  <div class="desktop-list">
    {#each events as event (event.slug)}
      <EventCard
        {event}
        onclick={() => eventSelectionSetter(event.slug)}
        isSelected={event.slug === selectedEventSlug}
      />
    {/each}
  </div>

  <!-- Mobile: single selected card with caret indicator -->
  {#if selectedEvent}
    <div class="mobile-card">
      <div class="mobile-card-inner">
        <EventCard
          event={selectedEvent}
          onclick={() => (showEventPicker = true)}
          isSelected={true}
        />
        <span class="mobile-caret" aria-hidden="true"></span>
      </div>
    </div>
  {/if}
</div>

<!-- Mobile: full-page event picker overlay -->
{#if showEventPicker}
  <div class="picker-overlay" transition:fly={{ y: -1000, duration: 300, easing: cubicOut }}>
    <div class="picker-header">
      <h2 class="picker-title">Choose an event</h2>
      <button class="picker-close" onclick={() => (showEventPicker = false)}>✕</button>
    </div>
    <div class="picker-list">
      {#each events as event (event.slug)}
        <EventCard
          {event}
          onclick={() => selectEvent(event.slug)}
          isSelected={event.slug === selectedEventSlug}
        />
      {/each}
    </div>
  </div>
{/if}

<style>
  /* --------------------------------------------- */
  /* ----------- Mobile-first defaults ----------- */
  /* --------------------------------------------- */

  .event-list-wrapper {
    display: flex;
    flex-direction: column;
    height: 100%;
  }

  /* Hidden on mobile; replaced by the single-card + picker pattern */
  .desktop-list {
    display: none;
  }

  .competition-label {
    display: none;
  }

  /* Single selected card shown on mobile */
  .mobile-card {
    display: block;
    width: 100%;
    border-bottom: 1px solid var(--brand);
  }

  .mobile-card-inner {
    position: relative;
  }

  /* The caret overlays the card's right edge, so push the card's results section
     (rendered inside EventCard, hence :global) clear of it */
  .mobile-card-inner :global(.event-results) {
    padding-right: 2.75rem;
  }

  .mobile-caret {
    position: absolute;
    right: 1.25rem;
    top: 50%;
    transform: translateY(-50%);
    width: 0;
    height: 0;
    border-left: 7px solid transparent;
    border-right: 7px solid transparent;
    border-top: 10px solid var(--text-muted);
    opacity: 0.45;
    pointer-events: none;
  }

  /* Full-page picker overlay (mobile only) */
  .picker-overlay {
    position: fixed;
    inset: 0;
    z-index: 9999; /* must sit above all page content including the navbar */
    background: var(--surface-card);
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }

  .picker-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1.25rem 1.25rem 0.875rem;
    border-bottom: 1px solid color-mix(in srgb, var(--text-primary) 10%, transparent);
    flex-shrink: 0;
    background: var(--surface-card);
  }

  .picker-title {
    font-size: 1rem;
    font-weight: 600;
    color: var(--text-primary);
    margin: 0;
  }

  .picker-close {
    background: none;
    border: none;
    cursor: pointer;
    font-size: 1rem;
    color: var(--text-muted);
    padding: 0.3rem 0.5rem;
    border-radius: 0.25rem;
    line-height: 1;
    transition: color 0.1s ease;
  }

  .picker-close:hover {
    color: var(--text-primary);
  }

  .picker-list {
    flex: 1;
    overflow-y: auto;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: thin;
    scrollbar-color: gray transparent;
  }

  /* --------------------------------------------- */
  /* ---------- Desktop style overrides ---------- */
  /* --------------------------------------------- */

  @media (min-width: 1024px) {
    .desktop-list {
      display: block;
      flex: 1;
      overflow-y: auto;
      min-height: 0;
      scrollbar-width: thin;
      scrollbar-color: var(--brand-tint) transparent;
    }

    .mobile-card {
      display: none;
    }

    .competition-label {
      display: block;
      text-align: center;
      font-size: 0.85rem;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--text-muted);
      padding: 1rem 1rem 0;
      flex-shrink: 0;
    }

    /* Hide the overlay even if somehow triggered on desktop */
    .picker-overlay {
      display: none;
    }
  }
</style>
