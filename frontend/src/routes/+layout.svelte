<script lang="ts">
  import '../app.css';
  import '$lib/fonts.css';
  import Navbar from '$lib/Navbar.svelte';
  let { children } = $props();
</script>

<Navbar />

{@render children()}
