import type { EventSlug } from './types.js';
import type {
  EventInfo,
  EventParticipationRecord,
  SolveInput,
  WeeklyCompetitionRecord
} from '../routes/compete/types.js';

/**
 * Storage context for the competition part of the application.
 *
 * Stores state which tracks the current/active compeition, which events are in the competition,
 * and records of the user's solves for each event.
 *
 * Also manages the submission of solves to the backend, and then updates this internal state
 * with an updated record of the user's participation in the various events, based on the
 * response from the solve submission API.
 */
export class CompetitionStore {
  competitionId = $state<string | null>(null);
  competitionName = $state('');
  weekLabel = $state('');
  weekTitle = $state('');
  events = $state<Record<EventSlug, EventInfo>>({} as Record<EventSlug, EventInfo>);
  userParticipation = $state<Record<string, EventParticipationRecord>>({});
  scrambles = $state<Record<string, string[]>>({});

  init(data: WeeklyCompetitionRecord): void {
    this.competitionId = data.id;
    this.competitionName = data.name;
    this.weekLabel = data.weekLabel;
    this.weekTitle = data.weekTitle;
    // The payload's events arrive as a list in display order; key them by slug for
    // direct lookup. The is safe in practice: only this competition's slugs are
    // present, and lookups always use a slug selected from this same payload.
    this.events = Object.fromEntries(data.events.map((e) => [e.slug, e])) as Record<
      EventSlug,
      EventInfo
    >;
    this.userParticipation = data.userParticipation;
    this.scrambles = data.scrambles;
  }

  /**
   * Submits a single solve to the backend to be recorded.
   *
   * The response contains an updated record of the user's participation in the event
   * they just submitted a solve for; once the event is complete, it's recorded as such,
   * and PB flags are evaluated in the backend and returned to the front here.
   */
  async submitSolve(eventSlug: EventSlug, solve: SolveInput): Promise<void> {
    const response = await fetch(
      `/api/competition/${this.competitionId}/events/${eventSlug}/solve`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(solve)
      }
    );

    const result: EventParticipationRecord = await response.json();
    this.userParticipation[eventSlug] = result;
  }
}
