<!--
@component
Card showing the user's solve results for a single event: a header with the event name,
format, and overall stats, above a table with one row per solve.
-->

<script lang="ts">
  import { formatBestSingle, formatEventResult, formatSolve } from '$lib/formatSolve.js';
  import type { EventInfo, EventParticipationRecord } from './types.js';
  import { RESULT_LABEL_BY_FORMAT } from './eventUtils.js';

  interface Props {
    participation: EventParticipationRecord | undefined;
    eventInfo: EventInfo;
  }

  const { participation, eventInfo }: Props = $props();

  // Number of solve rows to show in the table, based on the event format
  const numSolveRows = $derived(eventInfo.numSolves);

  // Once the event is complete, we show both the overall event result (mean, average),
  // and also the best single time. However, a "best of N" event's result IS the best single,
  // so the separate single row is omitted.
  const isBestOf = $derived(
    eventInfo.format === 'bo1' || eventInfo.format === 'bo3' || eventInfo.format === 'bo5'
  );

  const resultDisplay = $derived(formatEventResult(participation, { shouldAppendPb: true }));
  const singleDisplay = $derived(formatBestSingle(participation, { shouldAppendPb: true }));
</script>

<div class="results-zone">
  <header class="event-header">
    <div class="event-heading">
      <h2 class="event-name">{eventInfo.name}</h2>
      <span class="event-format">{eventInfo.format}</span>
    </div>
    <div class="event-stats">
      <div class="stat">
        <span class="stat-label">{RESULT_LABEL_BY_FORMAT[eventInfo.format]}</span>
        <span class="stat-value">{resultDisplay}</span>
      </div>
      {#if !isBestOf}
        <div class="stat">
          <span class="stat-label">single</span>
          <span class="stat-value">{singleDisplay}</span>
        </div>
      {/if}
    </div>
  </header>
  <div class="table-wrapper">
    <table class="solves-table">
      <thead>
        <tr>
          <th>#</th>
          <th>Time</th>
        </tr>
      </thead>
      <tbody>
        {#each Array.from({ length: numSolveRows }, (_, i) => i) as i (i)}
          {@const solve = participation?.solves[i]}
          <tr>
            <td class="rank-cell"><span class="rank-plain">{i + 1}</span></td>
            <td class={['mono', solve?.pbSingle && 'pb']}>
              {solve
                ? formatSolve(solve, { showParensForOmitted: true, shouldAppendPb: true })
                : '-'}
            </td>
          </tr>
        {/each}
      </tbody>
    </table>
  </div>
</div>

<style>
  /* --------------------------------------------- */
  /* ----------- Mobile-first defaults ----------- */
  /* --------------------------------------------- */

  .results-zone {
    flex: 1;
    min-width: 0;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    background: var(--surface-card);
    border-radius: 0.375rem;
    border: 1px solid color-mix(in srgb, var(--text-primary) 8%, transparent);
  }

  .event-header {
    display: flex;
    flex-wrap: wrap;
    align-items: baseline;
    gap: 0.375rem 0.75rem;
    padding: 0.875rem 0.625rem 0.75rem;
    border-bottom: 1px solid color-mix(in srgb, var(--text-primary) 10%, transparent);
  }

  .event-heading {
    display: flex;
    align-items: baseline;
    gap: 0.5rem;
  }

  .event-name {
    margin: 0;
    font-size: 1.05rem;
    font-weight: 700;
    color: var(--text-primary);
    line-height: 1.2;
  }

  .event-format {
    padding: 0.15rem 0.5rem;
    border-radius: 9999px; /* oversized radius = fully rounded pill */
    font-size: 0.6rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--brand);
    background: color-mix(in srgb, var(--brand) 12%, transparent);
  }

  .event-stats {
    margin-left: auto;
    display: flex;
    align-items: baseline;
    gap: 1rem;
  }

  .stat {
    display: flex;
    align-items: baseline;
    gap: 0.375rem;
  }

  .stat-label {
    font-size: 0.6rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--text-muted);
  }

  .stat-value {
    font-family: monospace;
    font-variant-numeric: tabular-nums;
    font-size: 0.85rem;
    color: var(--text-primary);
  }

  .table-wrapper {
    flex: 1;
    overflow-y: auto;
    padding: 0 0.5rem 1rem;
  }

  .solves-table {
    width: 100%;
    border-collapse: collapse;
  }

  .solves-table thead tr {
    position: sticky;
    top: 0;
    background: var(--surface-card);
    z-index: 1;
  }

  .solves-table th {
    text-align: left;
    padding: 1.5rem 0.625rem 0.5rem;
    font-size: 0.6rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    color: var(--text-muted);
    border-bottom: 1px solid color-mix(in srgb, var(--text-primary) 10%, transparent);
    white-space: nowrap;
  }

  .solves-table td {
    padding: 0.45rem 0.625rem;
    border-bottom: 1px solid color-mix(in srgb, var(--text-primary) 5%, transparent);
    font-size: 0.8rem;
    color: var(--text-primary);
    white-space: nowrap;
  }

  .solves-table tbody tr:hover {
    background: color-mix(in srgb, var(--brand) 4%, transparent);
  }

  .rank-cell {
    text-align: center;
    width: 2.25rem;
    padding-left: 0;
    padding-right: 0;
  }

  .rank-plain {
    font-size: 0.72rem;
    color: var(--text-muted);
  }

  .mono {
    font-family: monospace;
    font-variant-numeric: tabular-nums;
  }

  .mono.pb {
    font-weight: 700;
    text-shadow: 0 0 0.35em var(--pb-glow);
  }

  /* --------------------------------------------- */
  /* ---------- Desktop style overrides ---------- */
  /* --------------------------------------------- */

  @media (min-width: 768px) {
    .event-header {
      padding: 1rem 1.25rem 0.875rem;
    }

    .table-wrapper {
      padding: 0 1.25rem 1rem;
    }
  }
</style>
