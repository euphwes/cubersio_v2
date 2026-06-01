<!--
@component
Two-column layout shell with a fixed sidebar (left slot) and a scrollable main area (right slot).
Stacks vertically on mobile; switches to side-by-side at >= 1024px.
-->

<div class="layout">
  <div class="body">
    <aside class="sidebar">
      <slot name="left" />
    </aside>

    <main class="content">
      <slot name="right" />
    </main>
  </div>
</div>

<style>
  /* --------------------------------------------- */
  /* ----------- Mobile-first defaults ----------- */
  /* --------------------------------------------- */

  .layout {
    display: flex;
    flex-direction: column;
    height: calc(100vh - 3.25rem); /* full viewport height, minus mobile navbar */
    min-height: 0; /* enable proper flex overflow behaviors */
  }

  .body {
    flex: 1 1 auto; /* fill remaining space */
    display: flex;
    flex-direction: column;
    min-height: 0; /* allow children to scroll */
  }

  .sidebar {
    flex: 0 0 auto;
    max-height: 25%;
    width: 100%;
    overflow: auto;
  }

  .content {
    flex: 1 1 auto;
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 0;
  }

  /* --------------------------------------------- */
  /* ---------- Desktop style overrides ---------- */
  /* --------------------------------------------- */

  @media (min-width: 1024px) {
    .layout {
      height: calc(100vh - 4rem); /* desktop navbar is taller */
    }

    .body {
      flex-direction: row;
    }

    .sidebar {
      width: max(350px, 20%);
      max-height: unset;
      height: 100%;
    }

    .content {
      flex: 1;
      height: 100%;
      min-height: unset;
    }
  }
</style>
