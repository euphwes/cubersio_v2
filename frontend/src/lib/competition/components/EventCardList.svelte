<script lang="ts">
  import EventCard from '$lib/competition/components/EventCard.svelte';
  import type { EventSlug } from '$lib/types.js';

  const {
    events,
    eventSelectionSetter,
    selectedEventSlug = '333'
  }: {
    events: EventSlug[];
    selectedEventSlug: EventSlug | undefined;
    eventSelectionSetter: (slug: EventSlug) => void;
  } = $props();
</script>

<div
  class="carousel carousel-center no-swipe no-scrollbar lg:carousel-vertical w-screen snap-mandatory overflow-x-auto scroll-smooth lg:w-full lg:overflow-x-visible"
>
  {#each events as event, i (event)}
    {@const prev_i = i === 0 ? events.length - 1 : i - 1}
    {@const next_i = i === events.length - 1 ? 0 : i + 1}

    {@const curr_slug = event}
    {@const prev_slug = events[prev_i]}
    {@const next_slug = events[next_i]}

    <div
      id="event_{curr_slug}"
      class="carousel-item relative box-border w-screen snap-center px-8 py-2 lg:mt-4 lg:w-full lg:px-4 lg:py-0"
    >
      <EventCard
        eventSlug={event}
        onclick={() => eventSelectionSetter(event)}
        isSelected={event == selectedEventSlug}
      />
      <div
        class="mobile-only-indicators absolute left-2 right-2 top-1/2 flex -translate-y-1/2 transform justify-between"
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

<style>
  /*
  Mobile-first approach template
  */

  .mobile-only-indicators .btn-circle {
    background-color: var(--accent-grey);
    border-color: var(--accent-grey);
    color: var(--text-color-dark);
  }

  .mobile-only-indicators .btn-circle:active {
    background-color: var(--med-grey);
    border-color: var(--med-grey);
    color: var(--text-color-light);
  }

  /* Disable horizontal panning and user scroll; keep programmatic scroll */
  .no-swipe {
    overflow-x: hidden; /* no horizontal swipe/drag */
    touch-action: pan-y; /* allow vertical gestures only */
    overscroll-behavior-x: contain;
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
  @media (min-width: 1024px) {
    .mobile-only-indicators {
      display: none;
    }

    /** give me lg:mt-4, but on the bottom, only for last item */
    .carousel-item:last-child {
      margin-bottom: calc(var(--spacing) * 4);
    }
  }
</style>
