<!--
@component

The Cubersio logo — a "C" shape made of 9 colored stickers.

Easter egg: clicking the icon starts constantly shuffling the sticker
colors. Clicking again stops and restores the original arrangement.
-->

<script lang="ts">
  const originalStickerState = [
    'grad-red',
    'grad-blue',
    'grad-yellow',
    'grad-green',
    'grad-white',
    'grad-orange',
    'grad-green',
    'grad-red',
    'grad-blue'
  ];

  let currentlyScrambling = $state(false);
  let scrambleIntervalId = $state(0);
  let stickerState = $state([...originalStickerState]);

  function scramble() {
    for (let i = stickerState.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [stickerState[i], stickerState[j]] = [stickerState[j], stickerState[i]];
    }
  }

  function handleIconClick() {
    currentlyScrambling = !currentlyScrambling;

    if (currentlyScrambling) {
      scrambleIntervalId = setInterval(() => {
        if (currentlyScrambling) {
          scramble();
        } else {
          clearInterval(scrambleIntervalId);
          stickerState = [...originalStickerState];
        }
      }, 500);
    } else {
      clearInterval(scrambleIntervalId);
      stickerState = [...originalStickerState];
    }
  }
</script>

<!-- svelte-ignore a11y_click_events_have_key_events a11y_no_static_element_interactions -->
<div
  class="icon"
  role="button"
  tabindex="0"
  onclick={handleIconClick}
  onkeydown={(e) => e.key === 'Enter' && handleIconClick()}
>
  <svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <filter id="c-shadow" x="-15%" y="-15%" width="130%" height="130%">
        <feGaussianBlur in="SourceAlpha" stdDeviation="3" result="blur" />
        <feOffset dx="2" dy="4" result="offset" />
        <feFlood flood-color="#000000" flood-opacity="0.65" result="color" />
        <feComposite in="color" in2="offset" operator="in" result="shadow" />
        <feMerge>
          <feMergeNode in="shadow" />
          <feMergeNode in="SourceGraphic" />
        </feMerge>
      </filter>

      <linearGradient id="gloss" x1="0.1" y1="0" x2="0.75" y2="1" gradientUnits="objectBoundingBox">
        <stop offset="0%" stop-color="white" stop-opacity="0.38" />
        <stop offset="35%" stop-color="white" stop-opacity="0.10" />
        <stop offset="100%" stop-color="white" stop-opacity="0" />
      </linearGradient>

      <radialGradient id="grad-red" cx="100" cy="100" r="92" gradientUnits="userSpaceOnUse">
        <stop offset="56%" stop-color="#ff9898" />
        <stop offset="100%" stop-color="#f25050" />
      </radialGradient>
      <radialGradient id="grad-yellow" cx="100" cy="100" r="92" gradientUnits="userSpaceOnUse">
        <stop offset="56%" stop-color="#faffaa" />
        <stop offset="100%" stop-color="#e8f550" />
      </radialGradient>
      <radialGradient id="grad-blue" cx="100" cy="100" r="92" gradientUnits="userSpaceOnUse">
        <stop offset="56%" stop-color="#88c8ff" />
        <stop offset="100%" stop-color="#4a8ef5" />
      </radialGradient>
      <radialGradient id="grad-white" cx="100" cy="100" r="92" gradientUnits="userSpaceOnUse">
        <stop offset="56%" stop-color="#ffffff" />
        <stop offset="100%" stop-color="#dedede" />
      </radialGradient>
      <radialGradient id="grad-green" cx="100" cy="100" r="92" gradientUnits="userSpaceOnUse">
        <stop offset="56%" stop-color="#90ffaa" />
        <stop offset="100%" stop-color="#50e860" />
      </radialGradient>
      <radialGradient id="grad-orange" cx="100" cy="100" r="92" gradientUnits="userSpaceOnUse">
        <stop offset="56%" stop-color="#ffd090" />
        <stop offset="100%" stop-color="#f0a840" />
      </radialGradient>

      <clipPath id="c-clip">
        <path
          d="M 170.4761 159.1365 A 92 92 0 1 1 170.4761 40.8635 L 139.8343 66.5750 A 52 52 0 1 0 139.8343 133.4250 Z"
        />
      </clipPath>
    </defs>

    <g filter="url(#c-shadow)">
      <!-- Dark C background -->
      <path
        d="M 170.4761 159.1365 A 92 92 0 1 1 170.4761 40.8635 L 139.8343 66.5750 A 52 52 0 1 0 139.8343 133.4250 Z"
        fill="#000000"
      />

      <!-- Sticker 0 (40° – 71°) -->
      <path
        d="M 170.4761 159.1365 A 92 92 0 0 1 129.7835 187.0456 L 116.8342 149.1997 A 52 52 0 0 0 139.8343 133.4250 Z"
        fill="url(#{stickerState[0]})"
      />
      <!-- Sticker 1 (71° – 102°) -->
      <path
        d="M 129.7835 187.0456 A 92 92 0 0 1 80.5232 189.9147 L 88.9914 150.8214 A 52 52 0 0 0 116.8342 149.1997 Z"
        fill="url(#{stickerState[1]})"
      />
      <!-- Sticker 2 (102° – 133°) -->
      <path
        d="M 80.5232 189.9147 A 92 92 0 0 1 36.8658 166.9184 L 64.3154 137.8234 A 52 52 0 0 0 88.9914 150.8214 Z"
        fill="url(#{stickerState[2]})"
      />
      <!-- Sticker 3 (133° – 164°) -->
      <path
        d="M 36.8658 166.9184 A 92 92 0 0 1 11.3699 124.6719 L 49.9047 113.9450 A 52 52 0 0 0 64.3154 137.8234 Z"
        fill="url(#{stickerState[3]})"
      />
      <!-- Sticker 4 (164° – 195°) -->
      <path
        d="M 11.3699 124.6719 A 92 92 0 0 1 11.3699 75.3281 L 49.9047 86.0550 A 52 52 0 0 0 49.9047 113.9450 Z"
        fill="url(#{stickerState[4]})"
      />
      <!-- Sticker 5 (195° – 226°) -->
      <path
        d="M 11.3699 75.3281 A 92 92 0 0 1 36.8658 33.0816 L 64.3154 62.1766 A 52 52 0 0 0 49.9047 86.0550 Z"
        fill="url(#{stickerState[5]})"
      />
      <!-- Sticker 6 (226° – 257°) -->
      <path
        d="M 36.8658 33.0816 A 92 92 0 0 1 80.5232 10.0853 L 88.9914 49.1786 A 52 52 0 0 0 64.3154 62.1766 Z"
        fill="url(#{stickerState[6]})"
      />
      <!-- Sticker 7 (257° – 288°) -->
      <path
        d="M 80.5232 10.0853 A 92 92 0 0 1 129.7835 12.9544 L 116.8342 50.8003 A 52 52 0 0 0 88.9914 49.1786 Z"
        fill="url(#{stickerState[7]})"
      />
      <!-- Sticker 8 (288° – 320°) -->
      <path
        d="M 129.7835 12.9544 A 92 92 0 0 1 170.4761 40.8635 L 139.8343 66.5750 A 52 52 0 0 0 116.8342 50.8003 Z"
        fill="url(#{stickerState[8]})"
      />
    </g>

    <!-- Gloss overlay -->
    <path
      d="M 170.4761 159.1365 A 92 92 0 1 1 170.4761 40.8635 L 139.8343 66.5750 A 52 52 0 1 0 139.8343 133.4250 Z"
      fill="url(#gloss)"
      clip-path="url(#c-clip)"
    />

    <!-- Divider strokes and outline -->
    <line
      x1="118.4528"
      y1="153.9304"
      x2="128.1649"
      y2="182.3149"
      stroke="#000000"
      stroke-width="7"
      stroke-linecap="round"
    />
    <line
      x1="87.9329"
      y1="155.7080"
      x2="81.5818"
      y2="185.0280"
      stroke="#000000"
      stroke-width="7"
      stroke-linecap="round"
    />
    <line
      x1="60.8842"
      y1="141.4603"
      x2="40.2970"
      y2="163.2815"
      stroke="#000000"
      stroke-width="7"
      stroke-linecap="round"
    />
    <line
      x1="45.0879"
      y1="115.2858"
      x2="16.1867"
      y2="123.3310"
      stroke="#000000"
      stroke-width="7"
      stroke-linecap="round"
    />
    <line
      x1="45.0879"
      y1="84.7142"
      x2="16.1867"
      y2="76.6690"
      stroke="#000000"
      stroke-width="7"
      stroke-linecap="round"
    />
    <line
      x1="60.8842"
      y1="58.5397"
      x2="40.2970"
      y2="36.7185"
      stroke="#000000"
      stroke-width="7"
      stroke-linecap="round"
    />
    <line
      x1="87.9329"
      y1="44.2920"
      x2="81.5818"
      y2="14.9720"
      stroke="#000000"
      stroke-width="7"
      stroke-linecap="round"
    />
    <line
      x1="118.4528"
      y1="46.0696"
      x2="128.1649"
      y2="17.6851"
      stroke="#000000"
      stroke-width="7"
      stroke-linecap="round"
    />
    <path
      d="M 170.4761 159.1365 A 92 92 0 1 1 170.4761 40.8635 L 139.8343 66.5750 A 52 52 0 1 0 139.8343 133.4250 Z"
      fill="none"
      stroke="#000000"
      stroke-width="6"
    />
  </svg>
</div>

<style>
  .icon {
    width: 46px;
    height: 46px;
    cursor: pointer;
  }
</style>
