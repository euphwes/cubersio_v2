<script lang="ts">
  import '../app.css';
  import '$lib/fonts.css';
  import { setContext } from 'svelte';
  import Navbar from '$lib/Navbar.svelte';
  import { NavigationLock } from '$lib/navigationLock.svelte.js';
  let { children } = $props();

  // Shared with the navbar and any route that needs to lock navigation (e.g. the compete
  // view while a solve is in progress)
  setContext('navigationLock', new NavigationLock());
</script>

<Navbar />

{@render children()}
