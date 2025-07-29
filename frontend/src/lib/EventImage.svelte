<script lang="ts">
  import { getImagePath } from './util/event_utils.js';

  const { eventSlug, solved = false } = $props<{
    solved: boolean;
    eventSlug?: string;
  }>();

  const imagePath = $derived(getImagePath(eventSlug, solved));
</script>

<img src={imagePath} alt="{eventSlug} image" />
