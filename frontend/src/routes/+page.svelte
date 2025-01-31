<script>
  import '../app.css';
  import EventCard from '$lib/EventCard.svelte';

  export let data;
</script>

<div class="app-container">
  <div style="justify-content: center!important; display: flex;">
    {#each data.events as event}
    <EventCard eventSlug={event} />
  {/each}
  </div>

</div>
