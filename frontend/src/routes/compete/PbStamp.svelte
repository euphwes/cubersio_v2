<!--
@component
Circular ink rubber stamp marking a personal best.

The stamp design is procedurally generated (ish), with some variation in:
- text
- symbol shapes
- outer circle shape
- inner circle shape
- ink color
- rotation
- scale

The above elements of the design are by hashing the provided `EventParticipation` and mapping
the result to one of the options.

A turbulence filter roughens the edges so it looks a bit like ink pressed onto the page.
-->

<script lang="ts">
  import type { EventParticipationRecord } from './types.js';
  import { hashObject } from '$lib/utils.js';

  interface Props {
    participation: EventParticipationRecord;
  }

  const { participation }: Props = $props();

  // Helper functions which hashes the user's EventParticipation to consistently select a random
  // value from the provided options. The `salt` param ensures the selections aren't correlated.
  const chooseValue = <T,>(salt: string, options: T[]): T => {
    return options[chooseIndex(salt, options.length - 1)];
  };
  const chooseIndex = (salt: string, n: number): number => {
    return hashObject({ participation, salt }, n);
  };

  // Styling options for the different attributes of the stamp which have variation.
  const TEXT_VARIANTS = [
    { label: 'PB!', fontSize: 9, includeAdornment: true },
    { label: 'Wow!', fontSize: 8, includeAdornment: true },
    { label: 'Record!', fontSize: 8, includeAdornment: true },
    { label: 'Incredible!', fontSize: 7, includeAdornment: false },
    { label: 'Personal Best!', fontSize: 7, includeAdornment: false }
  ];

  const INK_COLORS = [
    '#133857',
    '#391a8d',
    '#4577a0',
    '#533b97',
    '#595c59',
    '#5e1375',
    '#627065',
    '#76637c'
  ];

  const SYMBOL_IDS = [
    'dotPath',
    'starPath',
    'boltPath',
    'plusPath',
    'cubePath',
    'heartPath',
    'diamondPath',
    'sparklePath',
    'trianglePath'
  ];

  const RING_SHAPE_IDS = [
    'plainArcPath',
    'plainArcPath',
    'wavyArcPath',
    'wavyArcPath',
    'zigzagArcPath',
    'dashedArcPath'
  ];

  const INNER_RING_SHAPE_IDS = [
    'plainInnerArcPath',
    'plainInnerArcPath',
    'wavyInnerArcPath',
    'wavyInnerArcPath',
    'dottedInnerArcPath'
  ];

  const BANNER_SHAPE_IDS = [
    'plainBannerPath',
    'plainBannerPath',
    'plainBannerPath',
    'wavyBannerPath'
  ];

  const RENDER_INNER_CIRCLE_OPTIONS = [true, true, true, false];

  // Choose values for this instance of the stamp.
  // Individual values are randomly-selected, but consistent for the same EventParticipation.

  // Choose from range [0, 40], shifted to [-20, 20] degrees
  const rotationDeg = $derived(chooseIndex('rotation', 40) - 20);

  // Choose range [0, 40], mapped to [1.2, 1.6] in 0.1 increments
  const scale = $derived(1.2 + chooseIndex('scale', 40) / 100);

  const inkColor = $derived(chooseValue('inkColor', INK_COLORS));
  const textVariant = $derived(chooseValue('text', TEXT_VARIANTS));
  const arcSymbol = $derived(chooseValue('arcSymbol', SYMBOL_IDS));
  const ringShape = $derived(chooseValue('ringShape', RING_SHAPE_IDS));
  const bannerSymbol = $derived(chooseValue('bannerSymbol', SYMBOL_IDS));
  const bannerShape = $derived(chooseValue('bannerShape', BANNER_SHAPE_IDS));
  const innerRingShape = $derived(chooseValue('innerRingShape', INNER_RING_SHAPE_IDS));
  const shouldRenderInnerCircle = $derived(chooseValue('innerCircle', RENDER_INNER_CIRCLE_OPTIONS));
</script>

<!-- Key on participation prop so the stamp remounts and replays its press-in
     animation each time it represents a different result (e.g. switching events) -->
{#key participation}
  <svg
    role="img"
    class="pb-stamp"
    viewBox="0 0 64 64"
    aria-label="Personal best"
    style:rotate="{rotationDeg}deg"
    style:scale
    style:--pb-ink={inkColor}
  >
    <title>Personal best!</title>
    <defs>
      <!-- Grain displacement roughens outlines, making this look like a worn stamp -->
      <filter id="stampFilter" x="-20%" y="-20%" width="140%" height="140%">
        <feTurbulence
          type="fractalNoise"
          baseFrequency="0.7"
          numOctaves="2"
          seed="4"
          result="grain"
        />
        <feDisplacementMap in="SourceGraphic" in2="grain" scale="0.80" result="rough" />
        <feTurbulence
          type="fractalNoise"
          baseFrequency="0.12"
          numOctaves="2"
          seed="11"
          result="blotch"
        />
        <feColorMatrix
          in="blotch"
          type="matrix"
          values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 1.2 0.30"
          result="wear"
        />
        <feComposite in="rough" in2="wear" operator="in" />
      </filter>
      <!-- Symbol paths, each centered on its own origin with a ~4.5-unit footprint -->
      <path
        id="starPath"
        d="M 0 -2.4 L .56 -.78 L 2.28 -.74 L .91 .3 L 1.41 1.94 L 0 .96 L -1.41 1.94 L -.91 .3 L -2.28 -.74 L -.56 -.78 Z"
      />
      <path id="dotPath" d="M 0 -1.7 A 1.7 1.7 0 1 1 0 1.7 A 1.7 1.7 0 1 1 0 -1.7 Z" />
      <path id="diamondPath" d="M 0 -2.2 L 1.6 0 L 0 2.2 L -1.6 0 Z" />
      <path
        id="sparklePath"
        d="M 0 -2.4 L .5 -.5 L 2.4 0 L .5 .5 L 0 2.4 L -.5 .5 L -2.4 0 L -.5 -.5 Z"
      />
      <path id="boltPath" d="M .9 -2.4 L -1.4 .3 H -.1 L -.9 2.4 L 1.4 -.4 H .1 Z" />
      <path
        id="cubePath"
        d="M -2.15 -2.15 h 1.9 v 1.9 h -1.9 Z M .25 -2.15 h 1.9 v 1.9 h -1.9 Z M -2.15 .25 h 1.9 v 1.9 h -1.9 Z M .25 .25 h 1.9 v 1.9 h -1.9 Z"
      />
      <path
        id="heartPath"
        d="M 0 2.0 C -0.6 1.2 -2.4 0.2 -2.4 -1.0 C -2.4 -2.2 -0.8 -2.4 0 -1.2 C 0.8 -2.4 2.4 -2.2 2.4 -1.0 C 2.4 0.2 0.6 1.2 0 2.0 Z"
      />
      <path
        id="plusPath"
        d="M -0.85 -2.3 h 1.7 v 1.45 h 1.45 v 1.7 h -1.45 v 1.45 h -1.7 v -1.45 h -1.45 v -1.7 h 1.45 Z"
      />
      <path id="trianglePath" d="M 0 -2.4 L 2.1 2.1 L -2.1 2.1 Z" />
      <!-- 
      Outer ring top-arc candidates:
      radius 26 centered on (32,32), spanning +/- 72 degrees from vertical
      -->
      <path id="plainArcPath" d="M 7.26 24 A 26 26 0 0 1 56.74 24" />
      <path
        id="wavyArcPath"
        d="M 7.27 23.97 L 7.13 22.45 L 7.43 21.06 L 8.27 19.91 L 9.48 19.00 L 10.73 18.19 L 11.69 17.25 L 12.29 16.04 L 12.68 14.60 L 13.17 13.17 L 14.00 12.01 L 15.24 11.30 L 16.72 10.97 L 18.19 10.73 L 19.45 10.26 L 20.49 9.40 L 21.42 8.25 L 22.45 7.13 L 23.69 6.42 L 25.11 6.27 L 26.59 6.57 L 28.03 6.95 L 29.38 7.04 L 30.67 6.67 L 32.00 6.00 L 33.39 5.40 L 34.81 5.25 L 36.17 5.69 L 37.41 6.57 L 38.56 7.50 L 39.76 8.13 L 41.09 8.32 L 42.58 8.25 L 44.09 8.27 L 45.45 8.70 L 46.51 9.66 L 47.28 10.97 L 47.96 12.29 L 48.80 13.35 L 49.93 14.07 L 51.32 14.60 L 52.70 15.24 L 53.76 16.19 L 54.34 17.49 L 54.52 19.00 L 54.60 20.49 L 54.93 21.79 L 55.68 22.91 L 56.73 23.97"
      />
      <path
        id="zigzagArcPath"
        d="M 7.27 23.97 L 7.85 19.70 L 11.86 17.36 L 12.84 12.84 L 17.36 11.86 L 19.70 7.85 L 24.31 8.32 L 27.76 5.23 L 32.00 7.10 L 36.24 5.23 L 39.69 8.32 L 44.30 7.85 L 46.64 11.86 L 51.16 12.84 L 52.14 17.36 L 56.15 19.70 L 56.73 23.97"
      />
      <path id="dashedArcPath" d="M 7.26 24 A 26 26 0 0 1 56.74 24" stroke-dasharray="4 2.5" />
      <!--
      Inner ring top-arc candidates:
      radius 21 centered on (32,32), spanning +/- 67 degrees from vertical
      -->
      <path id="plainInnerArcPath" d="M 12.58 24 A 21 21 0 0 1 51.42 24" />
      <path
        id="wavyInnerArcPath"
        d="M 12.58 24.00 L 12.79 22.88 L 13.22 21.85 L 13.90 20.95 L 14.74 20.17 L 15.56 19.42 L 16.27 18.60 L 16.85 17.66 L 17.43 16.68 L 18.13 15.79 L 19.01 15.11 L 20.05 14.64 L 21.12 14.28 L 22.13 13.86 L 23.06 13.29 L 23.95 12.60 L 24.89 11.96 L 25.93 11.53 L 27.04 11.38 L 28.18 11.42 L 29.29 11.48 L 30.38 11.40 L 31.45 11.15 L 32.55 10.86 L 33.68 10.73 L 34.79 10.88 L 35.85 11.28 L 36.86 11.78 L 37.87 12.20 L 38.93 12.45 L 40.05 12.60 L 41.17 12.82 L 42.20 13.25 L 43.10 13.93 L 43.87 14.76 L 44.62 15.59 L 45.44 16.30 L 46.38 16.89 L 47.35 17.47 L 48.24 18.17 L 48.92 19.06 L 49.38 20.09 L 49.75 21.16 L 50.17 22.18 L 50.74 23.10 L 51.42 24.00"
      />
      <path
        id="dottedInnerArcPath"
        d="M 12.58 24 A 21 21 0 0 1 51.42 24"
        stroke-width="1.4"
        stroke-linecap="round"
        stroke-dasharray="0.4 3.4"
      />
      <!--
      Banner bar top-line candidates:
      horizontal from x=2 to x=62 at y=25.5
      The bottom bar reuses the same path rotated 180 degrees about the center.
      -->
      <path id="plainBannerPath" d="M 2 25.5 H 62" />
      <path
        id="wavyBannerPath"
        d="M 2.00 25.50 L 3.20 25.97 L 4.40 26.26 L 5.60 26.26 L 6.80 25.97 L 8.00 25.50 L 9.20 25.03 L 10.40 24.74 L 11.60 24.74 L 12.80 25.03 L 14.00 25.50 L 15.20 25.97 L 16.40 26.26 L 17.60 26.26 L 18.80 25.97 L 20.00 25.50 L 21.20 25.03 L 22.40 24.74 L 23.60 24.74 L 24.80 25.03 L 26.00 25.50 L 27.20 25.97 L 28.40 26.26 L 29.60 26.26 L 30.80 25.97 L 32.00 25.50 L 33.20 25.03 L 34.40 24.74 L 35.60 24.74 L 36.80 25.03 L 38.00 25.50 L 39.20 25.97 L 40.40 26.26 L 41.60 26.26 L 42.80 25.97 L 44.00 25.50 L 45.20 25.03 L 46.40 24.74 L 47.60 24.74 L 48.80 25.03 L 50.00 25.50 L 51.20 25.97 L 52.40 26.26 L 53.60 26.26 L 54.80 25.97 L 56.00 25.50 L 57.20 25.03 L 58.40 24.74 L 59.60 24.74 L 60.80 25.03 L 62.00 25.50"
      />
      <path id="dashedBannerPath" d="M 2 25.5 H 62" stroke-dasharray="8 5" />
    </defs>

    <g class="ink" filter="url(#stampFilter)">
      <!-- Outer and inner arc pairs that stop short of the banner -->
      <use href="#{ringShape}" class="ring" stroke-width="2.8" />
      <use href="#{ringShape}" class="ring" stroke-width="2.8" transform="rotate(180 32 32)" />

      {#if shouldRenderInnerCircle}
        <use href="#{innerRingShape}" class="ring" stroke-width="1.6" />
        <use
          href="#{innerRingShape}"
          class="ring"
          stroke-width="1.6"
          transform="rotate(180 32 32)"
        />
      {/if}

      <!-- Symbol arcs, top, then bottom -->
      {#if shouldRenderInnerCircle}
        <use href="#{arcSymbol}" transform="translate(21.71 19.74) rotate(140)" />
        <use href="#{arcSymbol}" transform="translate(32 16) rotate(180)" />
        <use href="#{arcSymbol}" transform="translate(42.29 19.74) rotate(220)" />
        <use href="#{arcSymbol}" transform="translate(21.71 44.26) rotate(40)" />
        <use href="#{arcSymbol}" transform="translate(32 48)" />
        <use href="#{arcSymbol}" transform="translate(42.29 44.26) rotate(-40)" />
      {:else}
        <!-- No inner ring, so the symbols move outward slightly -->
        <use href="#{arcSymbol}" transform="translate(20.11 17.83) rotate(140) scale(1.2)" />
        <use href="#{arcSymbol}" transform="translate(32 13.5) rotate(180) scale(1.4)" />
        <use href="#{arcSymbol}" transform="translate(43.89 17.83) rotate(220) scale(1.2)" />
        <use href="#{arcSymbol}" transform="translate(20.11 46.17) rotate(40) scale(1.2)" />
        <use href="#{arcSymbol}" transform="translate(32 50.5) scale(1.4)" />
        <use href="#{arcSymbol}" transform="translate(43.89 46.17) rotate(-40) scale(1.2)" />
      {/if}

      <!-- Banner across the middle -->
      <use href="#{bannerShape}" class="banner" stroke-width="3" />
      <use href="#{bannerShape}" class="banner" stroke-width="3" transform="rotate(180 32 32)" />
      {#if textVariant.includeAdornment}
        <use href="#{bannerSymbol}" transform="translate(8 32) scale(1.4)" />
        <use href="#{bannerSymbol}" transform="translate(56 32) scale(1.4)" />
      {/if}

      <text
        class="stamp-text"
        x="32"
        y="32"
        font-size={textVariant.fontSize}
        text-anchor="middle"
        dominant-baseline="central"
        transform="translate(0 -0.5)"
      >
        {textVariant.label}
      </text>
    </g>
  </svg>
{/key}

<style>
  .pb-stamp {
    width: 1.6em;
    height: 1.6em;
    margin-left: var(--pb-stamp-gap, 0.5rem);
    vertical-align: -0.45em;
  }

  .ink {
    fill: var(--pb-ink);
  }

  .ring,
  .banner {
    fill: none;
    stroke: var(--pb-ink);
  }

  .stamp-text {
    font-weight: 900;
    letter-spacing: 0.05em;
  }

  /* One-shot press-down entrance so the stamp looks like it was just inked;
     skipped for reduced-motion users */
  @media (prefers-reduced-motion: no-preference) {
    .pb-stamp {
      animation: stamp-press 0.3s ease-out both;
    }
  }

  @keyframes stamp-press {
    from {
      transform: scale(1.5);
      opacity: 0;
    }
    70% {
      transform: scale(0.95);
      opacity: 1;
    }
    to {
      transform: scale(1);
      opacity: 1;
    }
  }
</style>
