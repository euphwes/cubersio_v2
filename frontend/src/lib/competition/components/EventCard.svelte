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
  import { nameByEventSlug } from '$lib/util/event_utils.js';
  import type { EventSlug } from '$lib/types.js';
  import EventImage from '$lib/shared/components/EventImage.svelte';

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
    <div class="event-title text-lg font-semibold">{eventName}</div>
    <div class="participant-count text-sm">{participantCount} competitors</div>
  </div>
</button>

<style>
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
    box-shadow:
      0 3px 6px rgba(0, 0, 0, 0.15),
      0 1px 2px rgba(0, 0, 0, 0.1);
  }

  .event-image-container {
    margin-left: 0.75rem;
    background-color: var(--med-grey);
    padding: 0.5rem;
  }

  .event-info-container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 0.5rem;
    padding-left: 1rem;
  }

  .event-title {
    color: var(--text-primary);
  }

  .participant-count {
    color: var(--text-secondary);
  }

  .event-image {
    width: 75px;
    height: 75px;
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
    .event-card.selected {
      background-color: var(--secondary-tint);
      border: 1px solid var(--secondary);
      color: var(--text-primary);
    }

    .event-card:hover {
      background-color: var(--surface-card-hover);
      border: 1px solid var(--surface-card-hover);
    }

    .event-card.selected:hover {
      background-color: var(--secondary-tint);
      border: 1px solid var(--secondary);
    }
  }
</style>
