<script lang="ts">
  import { page } from '$app/state';

  import CubersioIcon from '$lib/shared/components/CubersioIcon.svelte';

  const menuItemsAndRoutes = [
    ['Compete', '/compete'],
    ['Leaderboard', '/leaderboard'],
    ['Practice', '/practice']
  ];

  const currentPath = $derived(page.url.pathname);
  const isSelected = (path: string) => currentPath === path;
</script>

<div class="navbar">
  <div class="navbar-start">
    <div class="lg:block" style="line-height: 0;">
      <CubersioIcon />
    </div>
  </div>
  <div class="navbar-center hidden lg:flex">
    <ul class="menu menu-horizontal">
      {#each menuItemsAndRoutes as textAndRoute}
        {@const menuText = textAndRoute[0]}
        {@const route = textAndRoute[1]}
        {@const isMenuSelected = isSelected(route)}
        {@const linkClass = isMenuSelected ? 'text-l px-2 selected' : 'text-l px-2'}

        <li class={linkClass}>
          <a href={route} class="menu-link">{menuText} </a>
        </li>
      {/each}
    </ul>
  </div>
  <div class="navbar-end">
    <div class="dropdown dropdown-end">
      <div tabindex="0" role="button" class="btn btn-ghost px-2 lg:hidden">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-6 w-6"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path stroke-linecap="round" stroke-width="2" d="M4 5h16M4 12h16M4 19h16" />
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
  </div>
</div>

<style>
  .navbar {
    color: var(--text-primary);
    background-color: var(--surface-card);
    height: 4rem;
    border-bottom: 1px solid var(--brand);
    box-shadow:
      0 4px 6px rgba(0, 0, 0, 0.15),
      0 1px 2px rgba(0, 0, 0, 0.1);
  }

  .selected > a {
    font-weight: 600;
    border-bottom-left-radius: 0;
    border-bottom-right-radius: 0;
    border-bottom: 2px solid var(--brand);
  }

  .dropdown-content {
    color: var(--text-primary);
  }
</style>
