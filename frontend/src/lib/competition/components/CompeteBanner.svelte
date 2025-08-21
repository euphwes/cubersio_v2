<!--
@component

TODO
-->

<script lang="ts">
  const { title }: { title: string } = $props();
</script>

<div class="compete-banner">
  <h1 class="text-bold text-center text-xl lg:text-2xl">{title}</h1>
</div>

<style>
  /*
    Mobile-first approach template
  */

  .compete-banner {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    background-color: var(--secondary-color);
    color: var(--text-color-dark);
  }

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
  }
</style>
