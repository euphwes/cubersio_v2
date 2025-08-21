<script lang="ts">
  import { page } from '$app/state';

  import CubersioIcon from '$lib/shared/components/CubersioIcon.svelte';

  const menuItemsAndRoutes = [
    ['Compete', '/compete'],
    ['Leaderboard', '/leaderboard'],
    ['Practice', '/practice']
  ];

  // Path options for the underline SVG below
  const wave = 'M0 3 Q 10 0 20 3 T 40 3 T 60 3 T 80 3 T 100 3';
  const zigZag = 'M0 6 L10 0 L20 6 L30 0 L40 6 L50 0 L60 6 L70 0 L80 6 L90 0 L100 6';
  const dashes = 'M0 3 H10 M15 3 H25 M30 3 H40 M45 3 H55 M60 3 H70 M75 3 H85 M90 3 H100';
  const underlinePath = wave;

  const currentPath = $derived(page.url.pathname);
  const isSelected = (path: string) => currentPath === path;
</script>

<div class="navbar">
  <div class="navbar-start">
    <div class="dropdown">
      <div tabindex="0" role="button" class="btn btn-ghost mr-2 px-2 lg:hidden">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-5 w-5"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path stroke-linecap="round" stroke-width="2" d="M10 6h12M10 12h12M10 18h12" />
          <circle cx="5" cy="6" r="1" />
          <circle cx="5" cy="12" r="1" />
          <circle cx="5" cy="18" r="1" />
        </svg>
      </div>
      <ul class="dropdown-content menu menu-lg bg-base-100 rounded-box z-1 mt-3 w-52 p-2 shadow">
        {#each menuItemsAndRoutes as textAndRoute}
          {@const menuText = textAndRoute[0]}
          {@const route = textAndRoute[1]}
          <li><a href={route}>{menuText}</a></li>
        {/each}
      </ul>
    </div>
    <div class="ml-2 mr-3 hidden lg:block" style="line-height: 0;">
      <CubersioIcon />
    </div>
    <div class="text-xl">cubers.io</div>
  </div>
  <div class="navbar-center hidden lg:flex">
    <ul class="menu menu-horizontal">
      {#each menuItemsAndRoutes as textAndRoute}
        {@const menuText = textAndRoute[0]}
        {@const route = textAndRoute[1]}
        <li class="text-l-and-a-half px-2">
          <a href={route} class="menu-link"
            >{menuText}
            {#if isSelected(route)}
              <svg class="underline-svg" viewBox="0 0 100 6" preserveAspectRatio="none">
                <path
                  d={underlinePath}
                  stroke="var(--accent-color)"
                  fill="transparent"
                  stroke-width="2"
                />
              </svg>
            {/if}
          </a>
        </li>
      {/each}
    </ul>
  </div>
  <div class="navbar-end"></div>
</div>

<style>
  .navbar {
    color: var(--text-color-light);
    background-color: var(--primary-color);
    height: 64px;
    flex-shrink: 0;
    box-shadow:
      0 4px 6px rgba(0, 0, 0, 0.15),
      0 1px 2px rgba(0, 0, 0, 0.1);
  }

  .dropdown-content {
    color: var(--text-color-dark);
  }

  .text-l-and-a-half {
    font-size: 18px;
  }

  /* underline only for center menu items (desktop) */
  .menu-link {
    position: relative;
  }

  .underline-svg {
    position: absolute;
    bottom: -4px;
    left: 0;
    width: 100%;
    height: 6px;
  }
</style>
