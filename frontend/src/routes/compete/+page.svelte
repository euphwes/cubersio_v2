<script lang="ts">
  import { setContext } from 'svelte';
  import type { EventSlug } from '$lib/types.js';
  import type { WeeklyCompetitionRecord } from './types.js';
  import { CompetitionStore } from '$lib/competition.svelte.js';
  import CompeteSidebar from './CompeteSidebar.svelte';
  import TwoColumnLayout from '$lib/TwoColumnLayout.svelte';
  import CompetitionTimerPanel from './CompetitionTimerPanel.svelte';

  interface Props {
    data: WeeklyCompetitionRecord;
  }
  const { data }: Props = $props();

  const store = new CompetitionStore();
  store.init(data);
  setContext('competition', store);

  let selectedEventSlug = $state<EventSlug>(data.events[0]?.slug ?? '333');

  function handleEventSelect(slug: EventSlug) {
    selectedEventSlug = slug;
  }
</script>

<TwoColumnLayout>
  <svelte:fragment slot="left">
    <!--
      We want to display the events in a consistent order, so use the raw API response's
      ordered list. The `CompetitionStore.events` is an object keyed by event slug and doesn't
      preserve order; it's just used for internal state management.
    -->
    <CompeteSidebar
      events={data.events}
      {selectedEventSlug}
      eventSelectionSetter={handleEventSelect}
      weekLabel={store.weekLabel}
      weekTitle={store.weekTitle}
    />
  </svelte:fragment>

  <svelte:fragment slot="right">
    <CompetitionTimerPanel {selectedEventSlug} />
  </svelte:fragment>
</TwoColumnLayout>
