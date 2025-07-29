<script lang="ts">
  import '../app.css';
  import EventCardList from '$lib/EventCardList.svelte';
  import TwoColumnLayout from '$lib/TwoColumnLayout.svelte';
  import HubLandingInfo from '$lib/HubLandingInfo.svelte';
  import type { EventSlug } from '$lib/types.js';

  const {
    data
  }: {
    data: {
      events: EventSlug[];
    };
  } = $props();

  let selectedEventSlug = $state<EventSlug | undefined>(undefined);
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
    />
  </svelte:fragment>

  <svelte:fragment slot="right">
    <HubLandingInfo {selectedEventSlug} competitionTitle={'July 2025 Week 4'} />
  </svelte:fragment>
</TwoColumnLayout>
