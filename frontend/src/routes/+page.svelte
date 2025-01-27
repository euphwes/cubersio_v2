<script>
  import { onMount } from 'svelte';

  let message = '';

  onMount(async () => {
    const response = await fetch('/api/');
    const responseData = await response.json();  // this is cleaner with Axios
    message = responseData.message;
  });
</script>

<h1>{message}</h1>
