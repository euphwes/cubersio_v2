<!--
@component
Scrollable list of event cards for the active competition.

On mobile the list is a horizontal snap-scroll carousel; on desktop (lg+) it
switches to a vertical carousel that fills the sidebar.  Keyboard/touch
navigation is disabled — the ❮ ❯ buttons handle mobile swiping instead, and
desktop users click directly.

Props:
- `events`              — ordered list of event slugs to display
- `selectedEventSlug`   — which event is currently active (drives card highlight
                          and solve-drawer visibility)
- `eventSelectionSetter` — called whenever the user picks a different event
- `competitionTitle`    — optional label shown above the list on desktop only
-->
<script lang="ts">
  import { slide } from 'svelte/transition';
  import EventCard from '$lib/competition/components/EventCard.svelte';
  import type { EventSlug } from '$lib/types.js';

  const {
    events,
    eventSelectionSetter,
    selectedEventSlug = '333',
    competitionTitle
  }: {
    events: EventSlug[];
    selectedEventSlug: EventSlug | undefined;
    eventSelectionSetter: (slug: EventSlug) => void;
    competitionTitle?: string;
  } = $props();
</script>

<div class="event-list-wrapper">
  {#if competitionTitle}
    <p class="competition-label">{competitionTitle}</p>
  {/if}

  <div
    class="carousel carousel-center no-swipe no-scrollbar md:carousel-vertical w-screen snap-mandatory overflow-x-auto scroll-smooth md:w-full md:overflow-x-visible"
  >
    {#each events as event, i (event)}
      {@const prev_i = i === 0 ? events.length - 1 : i - 1}
      {@const next_i = i === events.length - 1 ? 0 : i + 1}

      {@const curr_slug = event}
      {@const prev_slug = events[prev_i]}
      {@const next_slug = events[next_i]}

      <div
        id="event_{curr_slug}"
        class="carousel-item relative box-border w-screen snap-center px-16 py-4 md:mt-4 md:w-full md:px-4 md:py-0"
      >
        <div class="card-stack {curr_slug === selectedEventSlug ? 'drawer-open' : ''}">
          <EventCard
            eventSlug={event}
            onclick={() => eventSelectionSetter(event)}
            isSelected={event == selectedEventSlug}
          />
          {#if curr_slug === selectedEventSlug}
            <div class="solve-drawer" transition:slide={{ duration: 250 }}>
              {#each [1, 2, 3, 4, 5] as slot}
                <div class="solve-slot">
                  <span class="solve-number">{slot}</span>
                  <span class="solve-time">—</span>
                </div>
              {/each}
            </div>
          {/if}
        </div>
        <div
          class="mobile-only-indicators absolute top-1/2 right-2 left-2 flex -translate-y-1/2 transform justify-between"
        >
          <a
            href="#event_{prev_slug}"
            class="btn btn-lg btn-circle"
            onclick={() => eventSelectionSetter(prev_slug)}>❮</a
          >
          <a
            href="#event_{next_slug}"
            class="btn btn-lg btn-circle"
            onclick={() => eventSelectionSetter(next_slug)}>❯</a
          >
        </div>
      </div>
    {/each}
  </div>
</div>

<style>
  .event-list-wrapper {
    display: flex;
    flex-direction: column;
    height: 100%;
  }

  .competition-label {
    display: none;
  }

  .mobile-only-indicators .btn-circle {
    background-color: var(--surface-card-selected);
    border-color: var(--secondary);
    color: var(--text-primary);
  }

  .mobile-only-indicators .btn-circle:active {
    background-color: var(--secondary);
    border-color: var(--secondary);
  }

  /* Disable horizontal panning and user scroll; keep programmatic scroll */
  .no-swipe {
    overflow-x: hidden; /* no horizontal swipe/drag */
    touch-action: pan-y; /* allow vertical gestures only */
    overscroll-behavior-x: contain;
  }

  .card-stack {
    display: flex;
    flex-direction: column;
    width: 100%;
  }

  /* Drawer hidden on mobile (horizontal carousel) */
  .solve-drawer {
    display: none;
  }

  /*
  sm (mobile)
  0 - 640px
  */
  @media (min-width: 640px) {
  }

  /*
  md (tablets, small laptops)
  641 - 768px
  */
  @media (min-width: 768px) {
  }

  /*
  lg (desktops)
  769 - 1024px
  */
  @media (min-width: 768px) {
    .mobile-only-indicators {
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

    /** give me lg:mt-4, but on the bottom, only for last item */
    .carousel-item:last-child {
      margin-bottom: calc(var(--spacing) * 4);
    }

    .solve-drawer {
      display: flex;
      flex-direction: column;
      gap: 0.3rem;
      padding: 0.5rem 0.5rem 0.625rem;
      background: var(--surface-card-hover);
      border: 1px solid color-mix(in srgb, var(--text-primary) 40%, transparent);
      border-radius: 0 0 0.25rem 0.25rem;
      width: 95%;
      align-self: center;
      margin-top: 0;
      overflow: hidden;
    }

    .card-stack.drawer-open > :global(.event-card) {
      box-shadow:
        0 6px 10px rgba(0, 0, 0, 0.18),
        0 2px 4px rgba(0, 0, 0, 0.1);
    }

    .solve-slot {
      display: flex;
      align-items: center;
      gap: 0.625rem;
      padding: 0.3rem 0.5rem;
      background: #ffffff;
      border: 1px solid color-mix(in srgb, var(--text-primary) 40%, transparent);
      border-radius: 0.2rem;
    }

    .solve-number {
      font-size: 0.7rem;
      font-weight: 600;
      color: var(--text-muted);
      width: 0.875rem;
      text-align: right;
      flex-shrink: 0;
    }

    .solve-time {
      font-size: 0.875rem;
      font-variant-numeric: tabular-nums;
      color: var(--text-primary);
      opacity: 0.4;
    }
  }
</style>
