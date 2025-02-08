<script>
  import '../app.css';
  import EventCard from '$lib/EventCard.svelte';

  export let data;
</script>

<div class="app-container">
  <div style="display: flex; flex-wrap: wrap; justify-content: center;">
    {#each data.events as event}
      <EventCard eventSlug={event} />
    {/each}
  </div>
</div>
