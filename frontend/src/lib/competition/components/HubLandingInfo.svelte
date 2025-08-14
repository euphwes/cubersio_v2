<!--
@component

TODO
-->

<script lang="ts">
  import type { EventSlug } from '$lib/types.js';
  import { nameByEventSlug, descriptionsByEventSlug } from '$lib/util/event_utils.js';
  import EventImage from '$lib/shared/components/EventImage.svelte';

  import Spacer from '$lib/shared/components/Spacer.svelte';
  import HorizontalDivider from '$lib/shared/components/HorizontalDivider.svelte';

  const { selectedEventSlug = '333' }: { selectedEventSlug: EventSlug } = $props();

  const description = $derived(selectedEventSlug ? descriptionsByEventSlug[selectedEventSlug] : '');
</script>

<div class="info-panel">
  <div class="event-info-container mt-12">
    <div class="event-title-row">
      <div class="event-image-container">
        <EventImage eventSlug={selectedEventSlug} solved={false} />
      </div>
      <h1 class="text-bold text-center text-4xl">{nameByEventSlug[selectedEventSlug]}</h1>
      <div class="event-image-container">
        <EventImage eventSlug={selectedEventSlug} solved={true} />
      </div>
    </div>
    <Spacer size="m" />
    <div class="event-description text-l text-center">
      <span>{description}</span>
    </div>
    <Spacer size="s" />
    <HorizontalDivider />
  </div>
  <div class="results-info-container"></div>
</div>

<style>
  /*
  Mobile-first approach template
  */

  .info-panel {
    height: calc(100% - 2rem); /* subtract vertical margins */
    color: var(--text-color-dark);
    margin: 1rem;
    border-radius: 0.5rem;
    transition: all 150ms ease;
    position: relative;
  }

  .event-title-row {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1rem;
    text-align: center;
  }

  .event-image-container {
    height: 2.5lh;
    aspect-ratio: 1 / 1;
  }

  .event-info-container {
    display: none;
  }

  .event-description {
    max-width: 75%;
    white-space: pre-wrap;
    line-height: 1.75;
    color: var(--med-grey);
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
    .info-panel {
      width: 80%;
    }

    .event-info-container {
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
    }
  }

  /*
  xl (wide monitors)
  1025+ px
  */
  @media (min-width: 1280px) {
  }
</style>
