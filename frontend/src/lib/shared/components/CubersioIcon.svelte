<!--
@component

Resembles the face of a 3x3 Rubik's Cube with the stickers in
a certain arrangement.

There's a small easter egg where clicking the cube enables or
disables a constant scrambling of the state of the stickers on
the cube face.
-->

<script lang="ts">
  // This is the starting arrangement of stickers on the cube,
  // which is also what the cube returns to once scrambling stops.
  let originalStickerState = [
    'bg-brand',
    'bg-brand',
    'bg-brand-tint',
    'bg-brand',
    'bg-brand-tint',
    'bg-secondary',
    'bg-brand-tint',
    'bg-secondary',
    'bg-secondary'
  ];

  let currentlyScrambling = $state(false);
  let scrambleIntervalId = $state(0);
  let stickerState = $state(originalStickerState);

  function scramble() {
    /**
     * Randomly reorder the elements of the provided array.
     * Used to "scramble" the stickers on the face of the cube.
     */
    for (let i = stickerState.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [stickerState[i], stickerState[j]] = [stickerState[j], stickerState[i]];
    }
  }

  function handleIconClick() {
    /**
     * Toggle whether we're currently scrambling.
     *
     * If we're now currently scrambling, set a recurring interval
     * to scramble the stickers every half second.
     *
     * If we're no longer scrambling, clear the interval and return
     * the stickers to their original state.
     */
    currentlyScrambling = !currentlyScrambling;

    if (currentlyScrambling) {
      scrambleIntervalId = setInterval(() => {
        if (currentlyScrambling) {
          scramble();
        } else {
          clearInterval(scrambleIntervalId);
          stickerState = originalStickerState;
        }
      }, 500);
    }
  }
</script>

<div class="cube">
  <img src="/images/cubersio_logo.svg" alt="cubersio logo" />
</div>

<style>
  .cube {
    width: 46px;
    height: 46px;
  }
  .cube div {
    width: 12px;
    height: 12px;
  }
  .bg-brand {
    background-color: var(--brand);
  }
  .bg-secondary {
    background-color: var(--secondary);
  }
  .bg-brand-tint {
    background-color: var(--brand-tint);
  }
</style>
