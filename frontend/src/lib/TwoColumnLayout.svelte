<div class="layout">
  <div class="banner">
    <slot name="banner" />
  </div>

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
    height: calc(100vh - 64px); /* full viewport height, minus navbar */
    min-height: 0; /* enable proper flex overflow behaviors */
  }

  /* Top banner: fixed percentage of viewport height, full width */
  .banner {
    flex: 0 0 6vh;
    width: 100%;
    overflow: hidden; /* clip anything tall */
  }

  /* Area below the banner */
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
  md (tablets, small laptops)
  641 - 768px
  */
  @media (min-width: 768px) {
  }

  /*
  lg (desktops)
  769 - 1024px
  */
  @media (min-width: 1024px) {
    /* keep column layout overall; only the body switches to two columns */
    .body {
      flex-direction: row;
    }

    /* Top banner: fixed percentage of viewport height, full width */
    .banner {
      flex: 0 0 8vh;
    }

    .sidebar {
      width: 25%;
      max-height: unset;
      height: 100%; /* fill remaining vertical space under banner */
    }

    .content {
      width: 75%;
      height: 100%; /* fill remaining vertical space under banner */
      min-height: unset;
    }
  }
</style>
