<!-- HorizontalDivider.svelte
 
TODO 
-->
<script lang="ts">
  import '../app.css';
</script>

<hr class="divider" />

<style>
  .divider {
    border: none;
    height: 1px;
    background: linear-gradient(to right, transparent, var(--secondary-color), transparent);
    margin: 1rem 0;
  }
</style>
