<script lang="ts">
  import TwoColumnLayout from '$lib/TwoColumnLayout.svelte';
</script>

<TwoColumnLayout>
  <svelte:fragment slot="left">
    <div class="placeholder"></div>
  </svelte:fragment>

  <svelte:fragment slot="right">
    <div class="placeholder"></div>
  </svelte:fragment>
</TwoColumnLayout>

<style>
  .placeholder {
    margin: 0.5rem;
    border-radius: 1rem;
    background-color: var(--surface-card-hover);
    height: calc(100% - 1rem);
    width: calc(100% - 1rem);
  }
</style>
