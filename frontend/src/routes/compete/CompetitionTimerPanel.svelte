<!--
@component
Main panel for the compete view. Contains the scramble bar, solve timer, submit/discard
actions, and a tabbed results area showing the user's solves and the event leaderboard.
-->

<script lang="ts">
  import type { EventSlug } from '$lib/types.js';
  import Timer from './Timer.svelte';
  import EventImage from './EventImage.svelte';

  interface Props {
    selectedEventSlug: EventSlug;
  }

  const { selectedEventSlug }: Props = $props();

  // TODO: replace with API-fetched scramble for the active event
  const scrambles = [
    "R U R' U' R U2 R' F R U R' U' F' R U R' U'",
    "F2 U' B2 D2 L2 F2 U' L2 B2 R' F D' R B U' L U2 F' U'",
    "D2 B2 U2 R2 B2 D R2 U F2 L2 U' F R' U2 B' R2 D F2 R' D2"
  ];
  let scrambleIndex = $state(0);
  const scramble = $derived(scrambles[scrambleIndex]);

  // Timer state
  let pendingSolveMs = $state<number | null>(null);
  let showSubmitDiscard = $state(false);

  // Results tabs
  type Tab = 'my-solves' | 'results';
  let activeTab = $state<Tab>('my-solves');

  // TODO: replace with real data from the API
  const mockResults = [
    {
      rank: 1,
      name: 'SpeedSolver42',
      avg: '8.23',
      best: '7.14',
      solves: ['7.45', '8.12', '9.13'],
      isMe: false
    },
    {
      rank: 2,
      name: 'CubeKing99',
      avg: '9.15',
      best: '8.32',
      solves: ['9.12', '8.32', '9.88'],
      isMe: false
    },
    {
      rank: 3,
      name: 'TwistMaster',
      avg: '9.87',
      best: '8.91',
      solves: ['8.91', '10.23', '9.45'],
      isMe: false
    },
    {
      rank: 4,
      name: 'LayerLord',
      avg: '11.23',
      best: '9.78',
      solves: ['11.45', '9.78', '12.45'],
      isMe: false
    },
    {
      rank: 5,
      name: 'PLL_Pro',
      avg: '12.01',
      best: '10.55',
      solves: ['12.45', '10.55', 'DNF'],
      isMe: false
    },
    {
      rank: 6,
      name: 'euphwes',
      avg: '14.23',
      best: '12.88',
      solves: ['14.23', '12.88', '—'],
      isMe: true
    },
    {
      rank: 7,
      name: 'CrossExpert',
      avg: '15.67',
      best: '14.22',
      solves: ['15.67', '14.22', '17.12'],
      isMe: false
    },
    {
      rank: 8,
      name: 'FingertrickFan',
      avg: '18.34',
      best: '16.77',
      solves: ['18.34', '16.77', '20.01'],
      isMe: false
    }
  ];

  // TODO: replace with real solve history from the API
  const mySolves = [
    { n: 1, time: '14.23' },
    { n: 2, time: '12.88', isPb: true },
    { n: 3, time: '—' }
  ];

  function handleTimerComplete(timeMs: number, _inspectionPenalty: boolean, dnf: boolean) {
    if (dnf) {
      pendingSolveMs = null;
      showSubmitDiscard = false;
      return;
    }
    pendingSolveMs = timeMs;
    showSubmitDiscard = true;
  }

  function handleTimerCancel() {
    pendingSolveMs = null;
    showSubmitDiscard = false;
  }

  function formatMs(ms: number): string {
    const totalSecs = Math.floor(ms / 1000);
    const centis = Math.floor((ms % 1000) / 10);
    if (totalSecs < 60) return `${totalSecs}.${centis.toString().padStart(2, '0')}`;
    const mins = Math.floor(totalSecs / 60);
    const secs = totalSecs % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}.${centis.toString().padStart(2, '0')}`;
  }

  function handleSubmit() {
    // TODO: POST solve to API
    pendingSolveMs = null;
    showSubmitDiscard = false;
  }

  function handleDiscard() {
    pendingSolveMs = null;
    showSubmitDiscard = false;
  }
</script>

<!-- Timer zone -->
<div class="compete-panel">
  <div class="timer-zone">
    <!-- Scramble bar -->
    <div class="scramble-bar">
      <p class="scramble-text">{scramble}</p>
      <div class="scramble-bar-preview">
        <EventImage eventSlug={selectedEventSlug} solved={false} />
      </div>
    </div>

    <!-- Timer -->
    <div class="timer-wrapper">
      <Timer
        onTimerComplete={handleTimerComplete}
        onTimerCancel={handleTimerCancel}
        onDnf={undefined}
      />
    </div>

    <!-- Action buttons -->
    <div class="timer-actions">
      {#if showSubmitDiscard}
        <button class="btn-action btn-submit" onclick={handleSubmit}>
          Submit {pendingSolveMs !== null ? formatMs(pendingSolveMs) : ''}
        </button>
        <button class="btn-action btn-discard" onclick={handleDiscard}>Discard</button>
      {/if}
    </div>
  </div>

  <!-- Bottom zone: tabbed results + scramble preview -->
  <div class="bottom-zone">
    <!-- Results box -->
    <div class="results-zone">
      <!-- Tab bar -->
      <div class="tab-bar">
        <button
          class="tab"
          class:active={activeTab === 'my-solves'}
          onclick={() => (activeTab = 'my-solves')}
        >
          My Solves
        </button>
        <button
          class="tab"
          class:active={activeTab === 'results'}
          onclick={() => (activeTab = 'results')}
        >
          Results
        </button>
      </div>

      <!-- Stats header: only shown on my-solves tab -->
      {#if activeTab === 'my-solves'}
        <div class="results-header">
          <!-- TODO: replace hardcoded stats with real event avg + best from API -->
          <div class="stat-chips">
            <div class="stat-chip">
              <span class="stat-label">Event avg</span>
              <span class="stat-value">11.43</span>
            </div>
            <div class="stat-chip">
              <span class="stat-label">Best time</span>
              <span class="stat-value">7.14</span>
            </div>
          </div>
        </div>
      {/if}

      <!-- Tab content -->
      <div class="table-wrapper">
        {#if activeTab === 'my-solves'}
          <table class="leaderboard">
            <thead>
              <tr>
                <th>#</th>
                <th>Time</th>
              </tr>
            </thead>
            <tbody>
              {#each mySolves as s}
                <tr>
                  <td class="rank-cell"><span class="rank-plain">{s.n}</span></td>
                  <td class="mono">
                    {s.time}
                    {#if s.isPb}<span class="pb-chip">pb</span>{/if}
                  </td>
                </tr>
              {/each}
            </tbody>
          </table>
        {:else}
          <table class="leaderboard">
            <thead>
              <tr>
                <th>#</th>
                <th>Competitor</th>
                <th>Avg of 5</th>
                <th>Best</th>
                <th>Solves</th>
              </tr>
            </thead>
            <tbody>
              {#each mockResults as row}
                <tr class:me-row={row.isMe}>
                  <td class="rank-cell">
                    {#if row.rank === 1}
                      <span class="rank-badge rank-gold">{row.rank}</span>
                    {:else if row.rank === 2}
                      <span class="rank-badge rank-silver">{row.rank}</span>
                    {:else if row.rank === 3}
                      <span class="rank-badge rank-bronze">{row.rank}</span>
                    {:else}
                      <span class="rank-plain">{row.rank}</span>
                    {/if}
                  </td>
                  <td class="name-cell">
                    {row.name}
                    {#if row.isMe}<span class="you-chip">you</span>{/if}
                  </td>
                  <td class="mono">{row.avg}</td>
                  <td class="mono">{row.best}</td>
                  <td class="mono">{row.solves.join(', ')}</td>
                </tr>
              {/each}
            </tbody>
          </table>
        {/if}
      </div>
    </div>

    <!-- Scramble preview image (desktop only) -->
    <div class="scramble-preview">
      <div class="scramble-preview-image">
        <EventImage eventSlug={selectedEventSlug} solved={false} />
      </div>
    </div>
  </div>
</div>

<style>
  /* --------------------------------------------- */
  /* ----------- Mobile-first defaults ----------- */
  /* --------------------------------------------- */

  /* Local color tokens for values not yet in the global design system */
  .compete-panel {
    --color-danger: #e53e3e;
    --color-pb: #38a169;

    position: relative;
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 100%;
    overflow: hidden;
    color: var(--text-primary);
  }

  /* ----- Timer zone ----- */

  .timer-zone {
    flex: 1;
    display: flex;
    flex-direction: column;
    padding: 0.75rem 1rem 0.625rem;
    gap: 0.5rem;
    border-bottom: 1px solid color-mix(in srgb, var(--text-primary) 10%, transparent);
    overflow: hidden;
    min-height: 0;
  }

  .scramble-bar {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    background: var(--surface-card);
    border: 1px solid color-mix(in srgb, var(--text-primary) 12%, transparent);
    border-radius: 0.375rem;
    padding: 0.5rem 0.625rem 0.5rem 0.875rem;
    flex-shrink: 0;
  }

  .scramble-text {
    flex: 1;
    margin: 0;
    font-family: monospace;
    font-size: 1.25rem;
    line-height: 1.5;
    color: var(--text-primary);
    word-break: break-word;
    text-align: left;
  }

  /* Shown on mobile alongside the scramble text */
  .scramble-bar-preview {
    display: block;
    width: 48px;
    height: 48px;
    flex-shrink: 0;
  }

  .timer-wrapper {
    flex: 1;
    display: flex;
    flex-direction: column;
    min-height: 0;
    /* Scales the timer display within this panel */
    --timer-font-size: 24vw;
  }

  .timer-actions {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    flex-shrink: 0;
  }

  .btn-action {
    padding: 0.375rem 1rem;
    border-radius: 0.375rem;
    font-size: 0.8rem;
    font-weight: 600;
    cursor: pointer;
    transition:
      background 0.15s ease,
      border-color 0.15s ease,
      color 0.15s ease;
  }

  .btn-submit {
    background: var(--brand);
    border: 1px solid var(--brand);
    color: #fff;
  }

  .btn-submit:hover {
    background: color-mix(in srgb, var(--brand) 82%, black);
  }

  .btn-discard {
    background: transparent;
    border: 1px solid color-mix(in srgb, var(--color-danger) 55%, transparent);
    color: var(--color-danger);
  }

  .btn-discard:hover {
    background: color-mix(in srgb, var(--color-danger) 8%, transparent);
  }

  /* ----- Bottom zone ----- */

  .bottom-zone {
    flex: 0 0 auto;
    height: 36vh;
    display: flex;
    flex-direction: row;
    gap: 0.75rem;
    padding: 0.75rem;
    overflow: hidden;
    min-height: 0;
  }

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

  /* Hidden on mobile; desktop shows it alongside the results table */
  .scramble-preview {
    display: none;
  }

  /* ----- Tab bar ----- */

  .tab-bar {
    display: flex;
    gap: 0.125rem;
    padding: 0 0.75rem;
    border-bottom: 1px solid color-mix(in srgb, var(--text-primary) 10%, transparent);
    flex-shrink: 0;
  }

  .tab {
    background: none;
    border: none;
    border-bottom: 2px solid transparent;
    padding: 0.6rem 0.625rem;
    font-size: 0.78rem;
    font-weight: 600;
    color: var(--text-muted);
    cursor: pointer;
    margin-bottom: -1px;
    transition:
      color 0.15s ease,
      border-color 0.15s ease;
  }

  .tab:hover {
    color: var(--text-primary);
  }

  .tab.active {
    color: var(--brand);
    border-bottom-color: var(--brand);
  }

  /* ----- Results header ----- */

  .results-header {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0.5rem 1rem;
    border-bottom: 1px solid color-mix(in srgb, var(--text-primary) 7%, transparent);
    flex-shrink: 0;
    gap: 2rem;
  }

  .stat-chips {
    display: flex;
    gap: 2rem;
    flex-shrink: 0;
  }

  .stat-chip {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.05rem;
  }

  .stat-label {
    font-size: 0.6rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--text-muted);
    opacity: 0.7;
  }

  .stat-value {
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--text-primary);
  }

  /* ----- Leaderboard table ----- */

  .table-wrapper {
    flex: 1;
    overflow-y: auto;
    padding: 0 0.5rem 1rem;
  }

  .leaderboard {
    width: 100%;
    border-collapse: collapse;
  }

  .leaderboard thead tr {
    position: sticky;
    top: 0;
    background: var(--surface-card);
    z-index: 1;
  }

  .leaderboard th {
    text-align: left;
    padding: 0.5rem 0.625rem;
    font-size: 0.6rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    color: var(--text-muted);
    border-bottom: 1px solid color-mix(in srgb, var(--text-primary) 10%, transparent);
    white-space: nowrap;
  }

  .leaderboard td {
    padding: 0.45rem 0.625rem;
    border-bottom: 1px solid color-mix(in srgb, var(--text-primary) 5%, transparent);
    font-size: 0.8rem;
    color: var(--text-primary);
    white-space: nowrap;
  }

  .leaderboard tbody tr:hover:not(.me-row) {
    background: color-mix(in srgb, var(--brand) 4%, transparent);
  }

  .me-row {
    background: color-mix(in srgb, var(--brand) 8%, transparent);
  }

  .rank-cell {
    text-align: center;
    width: 2.25rem;
    padding-left: 0;
    padding-right: 0;
  }

  .rank-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 1.4rem;
    height: 1.4rem;
    border-radius: 50%;
    font-size: 0.65rem;
    font-weight: 700;
  }

  .rank-gold {
    background: #f6d860;
    color: #5c3d00;
  }

  .rank-silver {
    background: #c0c0c0;
    color: #383838;
  }

  .rank-bronze {
    background: #cd7f32;
    color: #fff;
  }

  .rank-plain {
    font-size: 0.72rem;
    color: var(--text-muted);
  }

  .name-cell {
    font-weight: 500;
  }

  /* Collapse the Solves column on mobile - too wide for small screens */
  .leaderboard th:nth-child(n + 5),
  .leaderboard td:nth-child(n + 5) {
    display: none;
  }

  /* ----- Chips ----- */

  .you-chip {
    display: inline-block;
    background: color-mix(in srgb, var(--brand) 15%, transparent);
    color: var(--brand);
    font-size: 0.58rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    padding: 0.1rem 0.3rem;
    border-radius: 0.2rem;
    margin-left: 0.35rem;
    vertical-align: middle;
  }

  .pb-chip {
    display: inline-block;
    background: color-mix(in srgb, var(--color-pb) 15%, transparent);
    color: var(--color-pb);
    font-size: 0.58rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    padding: 0.1rem 0.3rem;
    border-radius: 0.2rem;
    margin-left: 0.35rem;
    vertical-align: middle;
  }

  .mono {
    font-family: monospace;
    font-variant-numeric: tabular-nums;
  }

  /* --------------------------------------------- */
  /* ---------- Desktop style overrides ---------- */
  /* --------------------------------------------- */

  @media (min-width: 768px) {
    .timer-zone {
      flex: 0 0 66%;
      padding: 1rem 1.5rem 0.75rem;
      gap: 0.75rem;
    }

    .scramble-text {
      font-size: 1.5rem;
      text-align: center;
    }

    /* On desktop the scramble preview moves to its own panel in the bottom zone */
    .scramble-bar-preview {
      display: none;
    }

    .timer-wrapper {
      min-height: 0;
      --timer-font-size: 12vw;
    }

    .bottom-zone {
      flex: 1;
      height: auto;
    }

    .scramble-preview {
      flex: 1;
      display: flex;
      align-items: center;
      justify-content: center;
      background: var(--surface-card);
      border-radius: 0.375rem;
      border: 1px solid color-mix(in srgb, var(--text-primary) 8%, transparent);
    }

    .scramble-preview-image {
      width: 180px;
      height: 180px;
    }

    .tab-bar {
      padding: 0 1.25rem;
    }

    .results-header {
      padding: 0.625rem 1.5rem;
    }

    .table-wrapper {
      padding: 0 1.25rem 1rem;
    }

    .leaderboard th:nth-child(n + 5),
    .leaderboard td:nth-child(n + 5) {
      display: table-cell;
    }
  }
</style>
