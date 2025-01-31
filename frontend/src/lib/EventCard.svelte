<!--
@component

EventCard

TODO
-->

<script lang="ts">
  const { eventSlug } = $props();
</script>

<div class="event-card drop-shadow ">
    <div class="event-image-container">
        <img class="event-image" src="/images/cube-{eventSlug}.png">
        <div class="overlay complete-overlay">
            <a href="#" class="icon"><i class="fas fa-check"></i></a>
        </div>
        <div class="overlay incomplete-overlay">
            <a href="#" class="icon"><i class="far fa-clock"></i></a>
        </div>
    </div>
    <div class="event-name">
        <hr>
        <div class="row">
            <div class="col-12"><span class="event-title">{eventSlug}</div>
        </div>
    </div>
    <span class="event-summary">Summary</span>
    <div class="bonus-event-indicator"><i class="fas fa-gift"></i></div>
</div>

<style>


.event-card {
    text-align: center;
    background-color: white;

    margin: 15px;
    padding: 15px;

    border-radius: 8px;
    
    -webkit-transition: all 250ms ease;
    -moz-transition: all 250ms ease;
    -o-transition: all 250ms ease;
    transition: all 250ms ease;

    position: relative;

    &.complete {
        .icon {
            color: desaturate(#3A8AAF, 15%);
        }
        .complete-overlay {
            opacity: 1;
            transition: all 250ms ease;
        }
    }

    &.incomplete {
        .icon {
            color: desaturate(#3A8AAF, 15%);
        }
        .incomplete-overlay {
            opacity: 1;
            transition: all 250ms ease;
        }
    }

    &.complete, &.incomplete {
        &:hover {
            .overlay {
                opacity: 0;
                transition: all 250ms ease;
            }
        }
    }

    &:hover {
        transform: translate(0px, -10px);

        -webkit-transition: all 250ms ease;
        -moz-transition: all 250ms ease;
        -o-transition: all 250ms ease;
        transition: all 250ms ease;

        .event-image {
            -webkit-filter: saturate(75%);
            filter: saturate(75%);
        }
    }
}

.event-image-container {

position: relative;
height: 110px;
width: 110px;

}

.event-image {
    -webkit-filter: saturate(0%) brightness(1.40);
    filter: saturate(0%) brightness(1.40);

    -webkit-transition: filter 250ms ease;
    -moz-transition: filter 250ms ease;
    -o-transition: filter 250ms ease;
    transition: filter 250ms ease;

    width: 100%;
    height: 100%;
}

.overlay {
position: absolute;
top: 0; bottom: 0; left: 0; right: 0;
opacity: 0;
transition: all 250ms ease;


}

.icon {
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    -ms-transform: translate(-50%, -50%);
    text-align: center;
    position: absolute;
  }


    span.event-title {
        font-size: 14px;
        font-family: 'Roboto', sans-serif;
    }

    span.event-summary {
        font-size: 12px;
        opacity: 0.66;
        position: absolute;
        right: 5px;
        bottom: 5px;
    }

.event-cards {
    justify-content: center!important;
}

.bonus-event-indicator {
    position: absolute;
    left: 5px;
    bottom: 5px;
    color: #9bd0db;
    font-size: 14px;
}
</style>
