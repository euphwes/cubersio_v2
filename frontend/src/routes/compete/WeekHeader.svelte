<!--
@component
Displays the competition week label and title at the top of the sidebar.
-->

<script lang="ts">
  interface Props {
    weekLabel: string;
    weekTitle: string;
  }

  const { weekLabel, weekTitle }: Props = $props();
</script>

<div class="week-header">
  <span class="week-label">{weekLabel}</span>
  <span class="week-title">{weekTitle}</span>
</div>

<style>
  .week-header {
    padding: 0.875rem 1rem 0.75rem;
    border-bottom: 1px solid color-mix(in srgb, var(--text-primary) 10%, transparent);
    flex-shrink: 0;
    text-align: center;
  }

  .week-label {
    display: block;
    font-size: 0.65rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--text-muted);
    opacity: 0.75;
  }

  .week-title {
    display: block;
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--text-primary);
    margin-top: 0.2rem;
  }
</style>
