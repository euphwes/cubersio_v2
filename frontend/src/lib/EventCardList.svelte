<script lang="ts">
  import '../app.css';
  import EventCard from '$lib/EventCard.svelte';
  import type { EventSlug } from './types.js';

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

<div class="event-card-list">
  {#each events as event (event)}
    <EventCard
      eventSlug={event}
      onclick={() => eventSelectionSetter(event)}
      isSelected={event == selectedEventSlug}
    />
  {/each}
</div>

<style>
  .event-card-list {
    padding: 1rem;
  }
</style>
