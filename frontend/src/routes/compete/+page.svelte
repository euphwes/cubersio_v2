<script lang="ts">
  import type { EventSlug } from '$lib/types.js';

  import CompeteSidebar from './CompeteSidebar.svelte';
  import TwoColumnLayout from '$lib/TwoColumnLayout.svelte';
  import CompetitionTimerPanel from './CompetitionTimerPanel.svelte';

  const {
    data
  }: {
    data: {
      events: EventSlug[];
    };
  } = $props();

  let selectedEventSlug = $state<EventSlug>('333');
  function handleEventSelect(slug: EventSlug) {
    selectedEventSlug = slug;
  }
</script>

<TwoColumnLayout>
  <svelte:fragment slot="left">
    <CompeteSidebar
      events={data.events}
      {selectedEventSlug}
      eventSelectionSetter={handleEventSelect}
      weekLabel="Week 24 · Jun 2026"
      weekTitle="Weekly Open"
    />
  </svelte:fragment>

  <svelte:fragment slot="right">
    <CompetitionTimerPanel {selectedEventSlug} />
  </svelte:fragment>
</TwoColumnLayout>
