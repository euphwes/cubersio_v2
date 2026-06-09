import type { EventParticipationRecord, SolveRecord } from '../routes/compete/types.js';

/**
 * Format a millisecond value as seconds with 2 decimals,
 * or if greater than 1 minute, as minutes + seconds with 2 decimals.
 */
function formatMs(ms: number): string {
  const totalSecs = Math.floor(ms / 1000);

  const centis = Math.floor((ms % 1000) / 10);
  const formattedCentis = centis.toString().padStart(2, '0');

  if (totalSecs < 60) {
    return `${totalSecs}.${formattedCentis}`;
  }

  const mins = Math.floor(totalSecs / 60);
  const secs = totalSecs % 60;
  const formattedSecs = secs.toString().padStart(2, '0');

  return `${mins}:${formattedSecs}.${formattedCentis}`;
}

interface FormatSolveOptions {
  /** Parenthesize solves omitted from the event average, per standard results notation */
  showParensForOmitted?: boolean;
  /** Append " (PB)" to solves flagged as a PB single */
  shouldAppendPb?: boolean;
}

/**
 * Human-friendly display for a solve.
 *
 * DNFs render as "DNF".
 * +2 solves display the effective time (recorded time plus the +2 penalty) with a trailing "+".
 *
 * See FormatSolveOptions for opt-in display decorations.
 */
export function formatSolve(solve: SolveRecord, options: FormatSolveOptions = {}): string {
  const { showParensForOmitted = false, shouldAppendPb = false } = options;
  let display: string;
  if (solve.dnf) {
    display = 'DNF';
  } else if (solve.timeMs === null) {
    return '—';
  } else if (solve.plusTwo) {
    display = `${formatMs(solve.timeMs + 2000)}+`;
  } else {
    display = formatMs(solve.timeMs);
  }
  if (showParensForOmitted && solve.omittedFromAverage) {
    display = `(${display})`;
  }
  return shouldAppendPb && solve.pbSingle ? `${display} (PB)` : display;
}

interface FormatStatOptions {
  /** Append " (PB)" when the stat is a personal best */
  shouldAppendPb?: boolean;
}

/**
 * Shared display logic for a an event's overall stats, like the mean/average/best single result
 * for the user's solves for a given event in a competition.
 *
 * Overall stats aren't "solves", but we display them similarly, so we make wrap them in an
 * object to make them look like a solve to we can reuse the same formatting utilities above.
 */
function formatStat(
  participation: EventParticipationRecord | undefined,
  ms: number | null,
  isPb: boolean
): string {
  if (ms === null) {
    return participation?.status === 'complete' ? 'DNF' : '-';
  }
  return formatSolve(
    {
      timeMs: ms,
      dnf: false,
      plusTwo: false,
      omittedFromAverage: false,
      pbSingle: isPb
    },
    { shouldAppendPb: true }
  );
}

/**
 * Display for the participation's overall result: the average/mean, or the best single
 * for best-of formats.
 */
export function formatEventResult(
  participation: EventParticipationRecord | undefined,
  { shouldAppendPb = false }: FormatStatOptions = {}
): string {
  const isPb = shouldAppendPb && (participation?.pbResult ?? false);
  return formatStat(participation, participation?.resultMs ?? null, isPb);
}

/**
 * Display for the participation's best single.
 */
export function formatBestSingle(
  participation: EventParticipationRecord | undefined,
  { shouldAppendPb = false }: FormatStatOptions = {}
): string {
  // The best single is a PB when any solve carries the pbSingle flag
  const isPb = shouldAppendPb && (participation?.solves.some((s) => s.pbSingle) ?? false);
  return formatStat(participation, participation?.bestMs ?? null, isPb);
}
