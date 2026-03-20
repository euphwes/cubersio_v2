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
    <div class="event-title text-base font-medium">{eventName}</div>
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
    margin-left: 0.5rem;
    background-color: var(--surface-image-bg);
    padding: 0.375rem;
  }

  .event-info-container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 0.25rem;
    padding-left: 0.625rem;
  }

  .event-title {
    color: var(--text-primary);
    font-size: 0.875rem;
  }

  .participant-count {
    color: var(--text-secondary);
    font-size: 0.75rem;
  }

  .event-image {
    width: 52px;
    height: 52px;
  }

  /*
  sm (mobile)
  0 - 640px
  */
  @media (min-width: 640px) {
  }

  /*
  md — sidebar is active here, so enable selected/hover states.
  Compact image and padding to fit the narrower 30% sidebar column.
  */
  @media (min-width: 768px) {
    .event-card.selected {
      background-color: var(--surface-card-selected);
      border: 1px solid var(--secondary);
      color: var(--text-primary);
    }

    .event-card:hover {
      background-color: var(--surface-card-hover);
      border: 1px solid var(--surface-card-hover);
    }

    .event-card.selected:hover {
      background-color: var(--surface-card-selected);
      border: 1px solid var(--secondary);
      color: var(--text-primary);
    }

    .event-image {
      width: 52px;
      height: 52px;
    }

    .event-image-container {
      margin-left: 0.5rem;
      padding: 0.375rem;
    }

    .event-info-container {
      padding-left: 0.625rem;
      gap: 0.25rem;
    }
  }

  /*
  lg — more room, but keep the leaner proportions from md.
  */
  @media (min-width: 1024px) {
    .event-image {
      width: 62px;
      height: 62px;
    }

    .event-image-container {
      margin-left: 0.625rem;
      padding: 0.4rem;
    }

    .event-info-container {
      padding-left: 0.75rem;
      gap: 0.3rem;
    }

    .event-title {
      font-size: 1rem;
    }

    .participant-count {
      font-size: 0.875rem;
    }
  }
</style>
