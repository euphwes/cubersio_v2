<!--
@component
Sidebar shell for the compete view.

Renders the competition title header and scrollable event card list.
The competition title header is hidden on mobile.
-->

<script lang="ts">
  import { getContext } from 'svelte';
  import type { EventSlug } from '$lib/types.js';
  import type { NavigationLock } from '$lib/navigationLock.svelte.js';
  import type { EventInfo } from './types.js';
  import WeekHeader from './WeekHeader.svelte';
  import EventCardList from './EventCardList.svelte';

  const navigationLock = getContext<NavigationLock>('navigationLock');

  interface Props {
    events: EventInfo[];
    selectedEventSlug: EventSlug;
    eventSelectionSetter: (slug: EventSlug) => void;
    weekLabel: string;
    weekTitle: string;
  }

  const { events, selectedEventSlug, eventSelectionSetter, weekLabel, weekTitle }: Props = $props();
</script>

<div class="compete-sidebar" class:locked={!navigationLock.navigationAllowed}>
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

  /* Disable event switching while a solve is in progress or awaiting submission */
  .compete-sidebar.locked {
    pointer-events: none;
    opacity: 0.4;
    transition: opacity 0.2s ease;
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
      border-right: 1px solid var(--brand-tint);
    }

    .sidebar-header {
      display: block;
    }
  }
</style>
