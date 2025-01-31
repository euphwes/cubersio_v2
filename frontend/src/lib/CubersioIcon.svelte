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
    'bg-cubersio-primary',
    'bg-cubersio-primary',
    'bg-cubersio-secondary',
    'bg-cubersio-primary',
    'bg-cubersio-secondary',
    'bg-cubersio-accent',
    'bg-cubersio-secondary',
    'bg-cubersio-accent',
    'bg-cubersio-accent'
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

<button class="cube" onclick={handleIconClick}>
  {#each stickerState as sticker}
    <div class="cubelet {sticker}"></div>
  {/each}
</button>

<style>
  .cube {
    width: 40px;
    height: 40px;
    display: inline-grid;
    grid-template-rows: repeat(3, 12px);
    grid-template-columns: repeat(3, 12px);
    gap: 2px;
    line-height: 0;
  }
  .cube div {
    width: 12px;
    height: 12px;
  }
  .cube > :nth-child(1) {
    border-top-left-radius: 4px;
  }
  .cube > :nth-child(3) {
    border-top-right-radius: 4px;
  }
  .cube > :nth-child(7) {
    border-bottom-left-radius: 4px;
  }
  .cube > :nth-child(9) {
    border-bottom-right-radius: 4px;
  }
</style>
