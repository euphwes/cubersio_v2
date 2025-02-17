<!--
@component

EventCard
7CB278
TODO
-->

<script lang="ts">
  const { eventSlug } = $props();
</script>

<div class="event-card drop-shadow">
  <div class="event-image-container">
    <img class="event-image" src="/images/{eventSlug}s.svg" alt="{eventSlug} image" />
  </div>
  <hr />
  <div class="event-title">{eventSlug}</div>
  <span class="event-summary">10.25</span>
</div>

<style>
  .event-card {
    text-align: center;
    background-color: #444444;
    margin: 1rem;
    padding: 1rem;
    border-radius: 0.5rem;
    transition: all 250ms ease;
    position: relative;
    box-shadow: 0 3px 6px rgba(0, 0, 0, 0.15), 0 1px 2px rgba(0, 0, 0, 0.1); /* Tighter, darker shadow */
  }

  .event-card:hover {
    transform: translate(0, -0.625rem);
    transition: all 250ms ease;
  }

  .event-card:hover .event-image {
    /* filter: saturate(75%);
    -webkit-filter: saturate(75%); */
  }

  .event-image-container {
    margin-bottom: 1rem;
  }

  .event-title {
    margin-top: 0.5rem;
  }

  .event-image {
    /* -webkit-filter: saturate(0%) brightness(1.4); */
    /* filter: saturate(0%) brightness(1.4); */

    -webkit-transition: filter 250ms ease;
    -moz-transition: filter 250ms ease;
    -o-transition: filter 250ms ease;
    transition: filter 250ms ease;

    /* width: 100%; */
    /* height: 100%; */
    width: 120px;
    height: 120px;
  }

  .event-summary {
    font-size: 0.75rem;
    opacity: 0.66;
    position: fixed;
    right: 0.25rem;
    bottom: 0.25rem;
  }
</style>
