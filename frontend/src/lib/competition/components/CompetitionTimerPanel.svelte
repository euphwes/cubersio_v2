<!--
@component
Right-pane compete panel: shows the event name, current scramble, timer, solve results, and scramble preview.
All content is static placeholder for now.
-->

<script lang="ts">
  import type { EventSlug } from '$lib/types.js';
  import EventImage from '$lib/shared/components/EventImage.svelte';
  import Timer from '$lib/shared/components/Timer.svelte';

  const { selectedEventSlug }: { selectedEventSlug: EventSlug } = $props();

  // Placeholder scramble — will eventually come from the server
  const scramble = "R U R' U' R U2 R' F R U R' U' F' R U R' U'";
</script>

<div class="compete-panel">
  <!-- Scramble -->
  <p class="scramble-text">{scramble}</p>

  <!-- Timer — front and center -->
  <Timer />

  <!-- Scramble preview — centered at the bottom -->
  <div class="scramble-preview">
    <p class="preview-label">Scramble preview</p>
    <div class="preview-image">
      <EventImage eventSlug={selectedEventSlug} solved={false} />
    </div>
  </div>
</div>

<style>
  .compete-panel {
    display: flex;
    flex-direction: column;
    height: 100%;
    width: 100%;
    padding: 3.25rem 1.5rem 1.5rem 1.5rem;
    gap: 1.25rem;
    color: var(--text-primary);
    box-sizing: border-box;
  }

  /* ── Scramble ── */
  .scramble-text {
    margin: 0;
    font-family: monospace;
    font-size: 2.5rem;
    line-height: 1.6;
    color: var(--text-primary);
    text-align: center;
    width: 85%;
    align-self: center;
    word-break: break-word;
  }

  /* ── Scramble preview — centered at bottom ── */
  .scramble-preview {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.375rem;
    align-self: center;
    flex-shrink: 0;
  }

  .preview-label {
    margin: 0;
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--text-muted);
  }

  .preview-image {
    height: calc((100vh - 4rem) * 0.25);
    width: calc((100vh - 4rem) * 0.25);
    padding: 0.5rem;
    background: color-mix(in srgb, var(--text-primary) 6%, transparent);
    border: 1px solid color-mix(in srgb, var(--text-primary) 10%, transparent);
    border-radius: 0.5rem;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  /* ── Mobile overrides (below lg breakpoint) ── */
  @media (max-width: 767px) {
    .compete-panel {
      padding: 1rem;
    }

    .scramble-text {
      font-size: 1.3rem;
      width: 100%;
    }

    .preview-image {
      width: auto;
      height: calc((100vh - 4rem) * 0.2);
      aspect-ratio: 1 / 1;
    }
  }
</style>
