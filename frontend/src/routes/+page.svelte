<script>
  export let data;
</script>

<h1>Events</h1>
{#each data.events as event}
  <div>{event}</div>
{/each}
