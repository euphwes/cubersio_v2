<script lang="ts">
  import type { EventSlug } from '$lib/types.js';

  import EventCardList from '$lib/competition/components/EventCardList.svelte';
  import TwoColumnLayout from '$lib/TwoColumnLayout.svelte';
  import EventInfoPanel from '$lib/competition/components/EventInfoPanel.svelte';

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
    <EventCardList
      events={data.events}
      eventSelectionSetter={handleEventSelect}
      {selectedEventSlug}
      competitionTitle="Aug 2025 · Week 3"
    />
  </svelte:fragment>

  <svelte:fragment slot="right">
    <EventInfoPanel {selectedEventSlug} />
  </svelte:fragment>
</TwoColumnLayout>
