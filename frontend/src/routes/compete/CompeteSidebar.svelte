<!--
@component
Sidebar shell for the compete view.

Renders the competition title header and scrollable event card list.
The competition title header is hidden on mobile.
-->

<script lang="ts">
  import type { EventSlug } from '$lib/types.js';
  import WeekHeader from './WeekHeader.svelte';
  import EventCardList from './EventCardList.svelte';

  interface Props {
    events: EventSlug[];
    selectedEventSlug: EventSlug;
    eventSelectionSetter: (slug: EventSlug) => void;
    weekLabel: string;
    weekTitle: string;
  }

  const { events, selectedEventSlug, eventSelectionSetter, weekLabel, weekTitle }: Props = $props();
</script>

<div class="compete-sidebar">
  <div class="sidebar-header">
    <WeekHeader {weekLabel} {weekTitle} />
  </div>
  <div class="sidebar-events">
    <EventCardList {events} {selectedEventSlug} {eventSelectionSetter} />
  </div>
</div>

<style>
  /* --------------------------------------------- */
  /* ----------- Mobile-first defaults ----------- */
  /* --------------------------------------------- */

  .compete-sidebar {
    display: flex;
    flex-direction: column;
    height: 100%;
    overflow: hidden;
    background: var(--surface-card);
  }

  /* Hidden on mobile; week header is desktop-only context */
  .sidebar-header {
    display: none;
    flex-shrink: 0;
  }

  .sidebar-events {
    flex: 1;
    min-height: 0;
    overflow-y: auto;
  }

  /* --------------------------------------------- */
  /* ---------- Desktop style overrides ---------- */
  /* --------------------------------------------- */

  @media (min-width: 1024px) {
    .compete-sidebar {
      border-right: 1px solid var(--brand);
    }

    .sidebar-header {
      display: block;
    }
  }
</style>
