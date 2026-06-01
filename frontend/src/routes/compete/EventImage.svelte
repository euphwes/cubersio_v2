<!--
@component
Displays the puzzle image for a given event, in either unsolved or solved state.
-->

<script lang="ts">
  import type { EventSlug } from '$lib/types.js';
  import { getImagePath } from './eventUtils.js';

  interface Props {
    eventSlug: EventSlug;
    solved?: boolean;
  }

  const { eventSlug, solved = false }: Props = $props();

  const imagePath = $derived(getImagePath(eventSlug, solved));
</script>

<img src={imagePath} alt="{eventSlug} image" />

<style>
  img {
    display: block;
    width: 100%;
    height: 100%;
    object-fit: contain;
  }
</style>
