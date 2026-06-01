<!--
@component
The cubers.io application navbar.

Provides navigation to the primary features of the site.

TODO: later, profile page, settings, buy me a cup of coffee, etc
-->

<script lang="ts">
  import { page } from '$app/state';
  import CubersioIcon from '$lib/CubersioIcon.svelte';

  const menuItemsAndRoutes: [string, string][] = [
    ['Compete', '/compete'],
    ['Practice', '/practice']
  ];

  const currentRoute = $derived(page.url.pathname);
  const getIsRouteSelected = (path: string) => currentRoute === path;

  let isMobileMenuOpen = $state(false);
  const closeMobileMenu = () => (isMobileMenuOpen = false);
  const toggleMobileMenu = () => (isMobileMenuOpen = !isMobileMenuOpen);
</script>

<nav class="navbar">
  <div class="navbar-start">
    <CubersioIcon />
    <span class="site-name">cubers.io</span>
  </div>

  <ul class="navbar-center">
    {#each menuItemsAndRoutes as [label, route]}
      <li>
        <a href={route} class="nav-link" class:selected={getIsRouteSelected(route)}>{label}</a>
      </li>
    {/each}
  </ul>

  <div class="navbar-end">
    <button
      class="hamburger-btn"
      aria-label="Toggle navigation menu"
      aria-expanded={isMobileMenuOpen}
      onclick={toggleMobileMenu}
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="24"
        height="24"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path stroke-linecap="round" stroke-width="2" d="M4 5h16M4 12h16M4 19h16" />
      </svg>
    </button>

    {#if isMobileMenuOpen}
      <ul class="mobile-menu">
        {#each menuItemsAndRoutes as [label, route]}
          <li>
            <a href={route} onclick={closeMobileMenu}>{label}</a>
          </li>
        {/each}
      </ul>
    {/if}
  </div>
</nav>

<style>
  @import url('https://fonts.googleapis.com/css2?family=Merriweather:wght@700&display=swap');

  /* --------------------------------------------- */
  /* ----------- Mobile-first defaults ----------- */
  /* --------------------------------------------- */

  .navbar {
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    align-items: center;
    padding: 0 1rem;
    height: 3.25rem;
    --icon-size: 40px;
    background-color: var(--surface-card);
    color: var(--text-primary);
    border-bottom: 1px solid var(--brand);
    box-shadow:
      0 4px 6px rgba(0, 0, 0, 0.15),
      0 1px 2px rgba(0, 0, 0, 0.1);
  }

  /* On mobile: visually indicate the nav is locked while the timer is running */
  :global(body.timer-active) .navbar {
    pointer-events: none;
    opacity: 0.4;
    transition: opacity 0.2s ease;
  }

  /* On desktop the overlay is hidden so the nav should stay fully interactive */
  @media (min-width: 1024px) {
    :global(body.timer-active) .navbar {
      pointer-events: auto;
      opacity: 1;
    }
  }

  .navbar-start {
    display: flex;
    align-items: center;
    gap: 0.625rem;
    line-height: 0;
  }

  .site-name {
    font-family: 'Merriweather', serif;
    font-size: 1.05rem;
    font-weight: 700;
    color: var(--text-primary);
    line-height: 1;
    /* Merriweather's cap height sits visually above the geometric center; nudge it down */
    transform: translateY(0.07em);
  }

  .navbar-center {
    display: none;
    align-items: center;
    list-style: none;
    margin: 0;
    padding: 0;
    gap: 0.25rem;
  }

  .nav-link {
    display: flex;
    align-items: center;
    padding: 0.5rem 0.75rem;
    border-radius: 0.375rem;
    font-size: 0.875rem;
    font-weight: 500;
    color: var(--text-primary);
    text-decoration: none;
    transition: background-color 0.1s ease;
  }

  .nav-link:hover {
    background-color: var(--surface-card-hover);
  }

  .nav-link.selected {
    font-weight: 600;
    border-radius: 0.375rem 0.375rem 0 0;
    border-bottom: 2px solid var(--brand);
  }

  .navbar-end {
    grid-column: 3;
    display: flex;
    align-items: center;
    justify-content: flex-end;
    position: relative;
  }

  .hamburger-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    background: none;
    border: none;
    cursor: pointer;
    padding: 0.5rem;
    border-radius: 0.375rem;
    color: var(--text-primary);
    transition: background-color 0.1s ease;
  }

  .hamburger-btn:hover {
    background-color: var(--surface-card-hover);
  }

  .mobile-menu {
    position: absolute;
    top: calc(100% + 0.5rem);
    right: 0;
    z-index: 50; /* above page content, below full-page overlays (9999) */
    list-style: none;
    margin: 0;
    padding: 0.5rem;
    min-width: 10rem;
    background: var(--surface-card);
    border: 1px solid color-mix(in srgb, var(--text-primary) 10%, transparent);
    border-radius: 0.5rem;
    box-shadow:
      0 4px 6px rgba(0, 0, 0, 0.15),
      0 1px 2px rgba(0, 0, 0, 0.1);
  }

  .mobile-menu a {
    display: block;
    padding: 0.625rem 1rem;
    border-radius: 0.375rem;
    font-size: 1rem;
    font-weight: 500;
    color: var(--text-primary);
    text-decoration: none;
    transition: background-color 0.1s ease;
  }

  .mobile-menu a:hover {
    background-color: var(--surface-card-hover);
  }

  /* --------------------------------------------- */
  /* ---------- Desktop style overrides ---------- */
  /* --------------------------------------------- */

  @media (min-width: 1024px) {
    .navbar {
      height: 4rem;
      --icon-size: 50px;
    }

    .navbar-center {
      display: flex;
    }

    .hamburger-btn {
      display: none;
    }
  }
</style>
