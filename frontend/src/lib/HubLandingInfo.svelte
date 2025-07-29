<!--
@component

TODO
-->

<script lang="ts">
  import '../app.css';

  import type { EventSlug } from './types.js';
  import { nameByEventSlug, getImagePath, descriptionsByEventSlug } from './util/event_utils.js';

  import Spacer from './Spacer.svelte';
  import HorizontalDivider from './HorizontalDivider.svelte';

  const { selectedEventSlug = '333' }: { selectedEventSlug: EventSlug } = $props();

  const description = $derived(selectedEventSlug ? descriptionsByEventSlug[selectedEventSlug] : '');
</script>

<div class="info-panel">
  <div class="event-info-container">
    <h1 class="text-bold text-center text-5xl">{nameByEventSlug[selectedEventSlug]}</h1>
    <Spacer size="m" />
    <div class="event-description text-center text-lg">
      {description}
    </div>
    <Spacer size="s" />
  </div>
  <HorizontalDivider />
</div>

<style>
  .info-panel {
    height: calc(100% - 2rem); /* subtract vertical margins */
    color: var(--text-color-dark);
    margin: 1rem;
    border-radius: 0.5rem;
    transition: all 150ms ease;
    position: relative;
  }

  .event-info-container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }

  .event-description {
    max-width: 75%;
    white-space: pre-wrap;
  }
</style>
