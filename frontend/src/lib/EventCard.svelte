<!--
@component

EventCard
TODO
-->

<script lang="ts">
  const { eventSlug } = $props();

  const nameByEventSlug = {
    '222': '2x2',
    '333': '3x3',
    '444': '4x4',
    '555': '5x5',
    '666': '6x6',
    '777': '7x7',
    '888': '8x8',
    '999': '9x9',
    '10x': '10x10',
    'pyra': 'Pyraminx',
    'skewb': 'Skewb',
    'sq1': 'Square-1',
    'clock': 'Clock',
    'mega': 'Megaminx',
    'kilo': 'Kilominx',
    '3bld': '3BLD',
    '4bld': '4BLD',
    '5bld': '5BLD',
    'mbld': '3x3 MBLD',
    'fto': 'FTO',
    'bump': 'Mirror Blocks',
    '3oh': '3x3 One-handed',
    'fmc': '3x3 Fewest Moves',
    'bicube': 'BiCube',
    'redi' : 'Redi Cube',
    '333relay': '3x3 Relay of 3',
    'dino' : 'Dino Cube',
    'rex' : 'Rex Cube',
    '15puzzle' : '15 Puzzle',
    '234relay' : '2-3-4 Relay',
    '332' : '3x3x2',
    '223' : '2x2x3',
    '334' : '3x3x4',
    '335' : '3x3x5',
  };
  const eventName = nameByEventSlug[eventSlug] || eventSlug;
</script>

<div class="event-card drop-shadow">
  <div class="event-image-container">
    <img class="event-image" src="/images/{eventSlug}.svg" alt="{eventSlug} image" />
  </div>
  <hr />
  <div class="event-title">{eventName}</div>
</div>

<style>
  .event-card {
    text-align: center;
    background-color: #555555;
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
    filter: saturate(75%);
    -webkit-filter: saturate(75%);
  }

  .event-image-container {
    margin-bottom: 1rem;
  }

  .event-title {
    margin-top: 0.5rem;
    color: #dfdfdf;
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

</style>
