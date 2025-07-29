<script lang="ts">
  import '../app.css';
  import CubersioIcon from '$lib/CubersioIcon.svelte';

  let { children } = $props();
</script>

<div class="navbar app-navbar">
  <div class="navbar-start">
    <div class="ml-2 mr-3" style="line-height: 0;">
      <CubersioIcon />
    </div>
    <a href="/">
      <div class="text-xl">cubers.io</div>
    </a>
  </div>
  <div class="navbar-center"></div>
  <div class="navbar-end"></div>
</div>

{@render children()}
