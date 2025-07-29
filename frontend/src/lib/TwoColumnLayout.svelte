<div class="layout">
  <aside class="sidebar">
    <slot name="left" />
  </aside>

  <main class="content">
    <slot name="right" />
  </main>
</div>

<style>
  .layout {
    display: flex;
    flex-direction: row;
    height: calc(100vh - 64px); /* full viewport height, minus navbar */
  }

  .sidebar {
    width: 25%;
    overflow-y: auto;
  }

  .content {
    width: 75%;
    height: 100%;
  }

  @media (max-width: 768px) {
    .layout {
      flex-direction: column;
    }

    .sidebar,
    .content {
      width: 100%;
    }
  }
</style>
