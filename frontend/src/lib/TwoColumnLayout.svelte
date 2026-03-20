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
  .layout {
    display: flex;
    flex-direction: column;
    height: calc(100vh - 4rem); /* full viewport height, minus navbar */
    min-height: 0; /* enable proper flex overflow behaviors */
  }

  .body {
    flex: 1 1 auto; /* fill remaining space */
    display: flex;
    flex-direction: column; /* stack on mobile */
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

  /*
  Mobile-first approach template
  */

  /*
  sm (mobile)
  0 - 640px
  */
  @media (min-width: 640px) {
  }

  /*
  md (tablets, small laptops) — two-column layout kicks in here.
  Sidebar is slightly wider (30%) to give event cards enough room.
  */
  @media (min-width: 768px) {
    /* keep column layout overall; only the body switches to two columns */
    .body {
      flex-direction: row;
    }

    .sidebar {
      width: 30%;
      max-height: unset;
      height: 100%; /* fill remaining vertical space under banner */
    }

    .content {
      width: 70%;
      height: 100%; /* fill remaining vertical space under banner */
      min-height: unset;
    }
  }

  /*
  lg (desktops) — revert to the standard 25/75 split now that there's enough room.
  */
  @media (min-width: 1024px) {
    .sidebar {
      width: 25%;
    }

    .content {
      width: 75%;
    }
  }
</style>
