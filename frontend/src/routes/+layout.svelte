<script lang="ts">
  import '$lib/../app.css';
  import Navbar from '$lib/shared/components/Navbar.svelte';
  let { children } = $props();
</script>

<Navbar />

{@render children()}
