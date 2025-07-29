<!--
@component

A clickable "card" for an event in the active competition.
Displays the event name and current competitor count alongside the event image.

Props:
- `onclick`: Callback invoked when this EventCard is clicked by the user.
- `eventSlug`: The internal slug representation of the event for this event.
- `participantCount`: (Optional) The number of competitors who have participated in this event
                      this week.
-->

<script lang="ts">
  import '../app.css';
  import { nameByEventSlug } from './util/event_utils.js';
  import type { EventSlug } from './types.js';
  import EventImage from './EventImage.svelte';

  interface IEventCardProps {
    onclick: () => void;
    eventSlug: EventSlug;
    participantCount?: number;
    isSelected: boolean;
  }
  const { eventSlug, onclick, participantCount = 132, isSelected }: IEventCardProps = $props();

  const eventName = nameByEventSlug[eventSlug] || eventSlug;
  const cardClass = $derived(isSelected ? 'event-card selected' : 'event-card');
</script>

<button class={cardClass} {onclick}>
  <div class="event-image-container">
    <div class="event-image">
      <EventImage {eventSlug} solved={false} />
    </div>
  </div>
  <div class="event-info-container text-left">
    <div class="event-title font-semibold">{eventName}</div>
    <div class="participant-count">{participantCount} competitors</div>
  </div>
</button>

<style>
  .event-card {
    display: flex;
    flex-direction: row;
    width: 100%;
    margin-bottom: 1rem;
    color: var(--text-color-dark);
    background-color: var(--surface-color-dark);
    border-radius: 0.5rem;
    transition: all 150ms ease;
    box-shadow:
      0 3px 6px rgba(0, 0, 0, 0.15),
      0 1px 2px rgba(0, 0, 0, 0.1);
  }

  .event-card.selected {
    background-color: var(--accent-color);
    transition: all 150ms ease;
  }

  .event-card:hover {
    transform: translate(0.5rem, 0);
    transition: all 150ms ease;
  }

  .event-image-container {
    margin-left: 0.75rem;
    background-color: var(--med-grey);
    padding: 0.5rem;
  }

  .event-info-container {
    display: flex;
    flex-direction: column;
    padding: 1rem;
  }

  .event-title {
    font-size: 1.25em;
  }

  .participant-count {
    font-size: 0.85em;
    margin-top: auto;
  }

  .event-image {
    width: 75px;
    height: 75px;
  }
</style>
