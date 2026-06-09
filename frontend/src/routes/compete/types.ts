import type { EventSlug } from '$lib/types.js';

/**
 * A single solve by a user within an event during a competition.
 */
export interface SolveRecord {
  // Elapsed time of the solve, measured in milliseconds. Is null for DNFs that
  // because the user's inspection time expired past the -2s threshold.
  timeMs: number | null;
  // Whether the solve is a DNF (did not finish).
  dnf: boolean;
  // Whether the solve carries a +2s penalty.
  plusTwo: boolean;
  // Whether this solve is excluded from the average (parenthesized in standard
  // results notation). False until the event's final solve is submitted, at which
  // point the flags are computed once and persisted with the solves.
  omittedFromAverage: boolean;
  // True on at most one solve per event: the fastest successful solve of the set,
  // when it beats the user's PB single from previous competitions. Evaluated and
  // persisted once, when the event's final solve is submitted; False until then.
  // DNFs are never PBs.
  pbSingle: boolean;
}

/**
 * A user's progress through a single event's solves
 */
export type ParticipationStatus = 'not_started' | 'in_progress' | 'complete';

/**
 * A user's overall participation in one event in one competition.
 *
 * Tracks their status for that event, lists the individual solves,
 * and contains their overall result; single, mean, and/or average,
 * depending on the event format.
 */
export interface EventParticipationRecord {
  status: ParticipationStatus;
  solves: SolveRecord[];
  // Backend-computed stats. resultMs is the format-appropriate result (average/mean
  // for ao5/mo3, best single for best-of formats; null while incomplete or DNF).
  // bestMs is redundant with resultMs for best-of formats, but kept as a tiebreaker
  // between tied averages/means
  resultMs: number | null;
  bestMs: number | null;
  // True once the event is complete and resultMs beats the user's best result for
  // this event from previous competitions
  pbResult: boolean;
}

/**
 * How an event's overall result is computed from its solves. Average formats drop
 * the best and worst solves and average the rest; mean formats average all solves;
 * best-of formats take the fastest single.
 */
export type EventFormat = 'ao5' | 'bo5' | 'mo3' | 'bo3' | 'bo1';

/**
 * Static details of one event within a competition.
 *
 * Identity and display info only; nothing user-specific lives here.
 */
export interface EventInfo {
  slug: EventSlug;
  name: string;
  format: EventFormat;
  // How many solves make a full set for this event; follows from the format
  // (5 for ao5/bo5, 3 for mo3/bo3, 1 for bo1)
  numSolves: number;
}

/**
 * Everything the compete page needs to render, in a single payload.
 *
 * Combines the identity and display details of a single weekly competition
 * with its events, the user's participation so far in each event, and the
 * scrambles for each event.
 */
export interface WeeklyCompetitionRecord {
  id: string;
  name: string;
  weekLabel: string;
  weekTitle: string;
  // In display order; the context storage re-keys these by slug in an object
  // for easy lookup.
  events: EventInfo[];
  userParticipation: Record<EventSlug, EventParticipationRecord>;
  // One scramble per expected solve for each event, keyed by event slug
  scrambles: Record<EventSlug, string[]>;
}

/**
 * A single solve as submitted to the backend; raw time and penalties only.
 *
 * Stats and PB flags are computed and persisted backend,
 * not accepted from the client.
 */
export interface SolveInput {
  timeMs: number | null;
  dnf: boolean;
  plusTwo: boolean;
}
