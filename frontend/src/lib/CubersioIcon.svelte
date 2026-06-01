<!--
@component
The cubers.io logo: a "C" superimposed on a colorful gradient square,
with a light grid pattern defining the face of a 3x3 cube.
-->

<div class="icon">
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="100%" height="100%">
    <defs>
      <!--
        top row gradient: blue to green
      -->
      <linearGradient id="topColors" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="#4591f5" />
        <stop offset="10%" stop-color="#4591f5" />
        <stop offset="90%" stop-color="#54fd64" />
        <stop offset="100%" stop-color="#54fd64" />
      </linearGradient>

      <!--
        bottom row gradient: red to orange
      -->
      <linearGradient id="bottomColors" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="#f45e5e" />
        <stop offset="10%" stop-color="#f45e5e" />
        <stop offset="90%" stop-color="#f8b468" />
        <stop offset="100%" stop-color="#f8b468" />
      </linearGradient>

      <!-- 
        vertical mask gradient, used to blend top row and bottom row gradients
      -->
      <linearGradient id="verticalMask" x1="0%" y1="0%" x2="0%" y2="100%">
        <stop offset="0%" stop-color="#000000" />
        <stop offset="10%" stop-color="#000000" />
        <stop offset="90%" stop-color="#FFFFFF" />
        <stop offset="100%" stop-color="#FFFFFF" />
      </linearGradient>

      <mask id="blendMask">
        <rect width="100%" height="100%" fill="url(#verticalMask)" />
      </mask>

      <!--
        drop shadow to elevate the "C" off the background
      -->
      <filter id="c-shadow" x="-20%" y="-20%" width="140%" height="140%">
        <feDropShadow dx="0" dy="25" stdDeviation="25" flood-color="#000000" flood-opacity="0.75" />
      </filter>
    </defs>

    <!--
      base layer, filled with the top colors gradient
    -->
    <rect width="100%" height="100%" rx="150" fill="url(#topColors)" />

    <!--
      overlay layer, using the vertical blend mask to show the top colors and the bottom colors
    -->
    <rect width="100%" height="100%" rx="150" fill="url(#bottomColors)" mask="url(#blendMask)" />

    <!--
      3x3 grid lines
    -->
    <g stroke="#ffffff" stroke-width="24" stroke-opacity="1">
      <line x1="0" y1="333" x2="1000" y2="333" />
      <line x1="0" y1="667" x2="1000" y2="667" />
      <line x1="333" y1="0" x2="333" y2="1000" />
      <line x1="667" y1="0" x2="667" y2="1000" />
    </g>

    <text
      x="500"
      y="500"
      class="center-text"
      text-anchor="middle"
      dominant-baseline="central"
      stroke="#000000"
      stroke-width="35"
      stroke-opacity="0.60"
      paint-order="stroke fill"
      filter="url(#c-shadow)">C</text
    >
  </svg>
</div>

<style>
  @import url('https://fonts.googleapis.com/css2?family=Merriweather:wght@700&amp;display=swap');

  .center-text {
    font-family: 'Merriweather', serif;
    font-size: 800px;
    font-weight: bold;
    fill: #ffffff;
  }

  .icon {
    width: var(--icon-size, 50px);
    height: var(--icon-size, 50px);
    cursor: pointer;
  }
</style>
