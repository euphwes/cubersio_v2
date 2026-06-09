from cubersio.events import SORT_INDEX_BY_EVENT_SLUG
from cubersio.models.competition import (
    EventInfo,
    EventParticipationRecord,
    SolveInput,
    SolveRecord,
    WeeklyCompetitionRecord,
)
from cubersio.services import solve_stats
from cubersio.services.competition_persistence import InMemoryCompetitionPersistence
from cubersio.services.exceptions import (
    CompetitionNotActiveException,
    EventAlreadyCompleteException,
    EventNotInCompetitionException,
)
from cubersio.types import EventSlug, ParticipationStatus


class CompetitionInterface:
    def __init__(self, persistence: InMemoryCompetitionPersistence) -> None:
        self._persistence = persistence

    def _derive_participation_status(
        self,
        solves: list[SolveRecord],
        target_solves_count: int,
    ) -> ParticipationStatus:
        if not solves:
            return ParticipationStatus.NOT_STARTED
        if len(solves) >= target_solves_count:
            return ParticipationStatus.COMPLETE
        return ParticipationStatus.IN_PROGRESS

    def _is_pb_result(
        self,
        event_slug: EventSlug,
        result_ms: int | None,
    ) -> bool:
        """
        Whether a completed event's result beats the user's best result for the event
        from previous competitions. A DNF result (None) is never a PB.
        """
        if result_ms is None:
            return False
        prior_pb = self._persistence.get_user_pb_result_ms(event_slug)
        return prior_pb is None or result_ms < prior_pb

    def get_competition_page(self) -> WeeklyCompetitionRecord:
        """Assembles everything the compete page needs into a single payload."""
        events = self._sorted_events(self._persistence.get_events())

        participation: dict[EventSlug, EventParticipationRecord] = {}
        for event_info in events:
            user_solves = self._persistence.get_user_solves(event_info.slug)
            status = self._derive_participation_status(user_solves, event_info.num_solves)
            result_ms = solve_stats.result_for_format(user_solves, event_info.format)
            participation[event_info.slug] = EventParticipationRecord(
                status=status,
                solves=user_solves,
                result_ms=result_ms,
                best_ms=solve_stats.best_time(user_solves),
                pb_result=self._persistence.get_pb_result_flag(event_info.slug),
            )

        competition = self._persistence.get_competition()

        return WeeklyCompetitionRecord(
            id=competition.id,
            name=competition.name,
            week_label=competition.week_label,
            week_title=competition.week_title,
            events=events,
            user_participation=participation,
            scrambles=self._persistence.get_scrambles(),
        )

    def submit_solve(
        self,
        competition_id: str,
        event_slug: EventSlug,
        solve_input: SolveInput,
    ) -> EventParticipationRecord:
        event_info = self._validate_submission(competition_id, event_slug)

        record = SolveRecord(
            time_ms=solve_input.time_ms,
            dnf=solve_input.dnf,
            plus_two=solve_input.plus_two,
        )
        updated_solves = self._persistence.add_solve(event_info.slug, record)
        status = self._derive_participation_status(updated_solves, event_info.num_solves)
        result_ms = solve_stats.result_for_format(updated_solves, event_info.format)

        # Omitted-solve and PB flags are point-in-time data, only final once the last
        # solve is in; they're evaluated and persisted exactly once, at completion,
        # rather than recomputed on every fetch of the solves
        if status is ParticipationStatus.COMPLETE:
            omitted_indices = solve_stats.omitted_solve_indices(
                updated_solves, event_info.format
            )
            updated_solves = self._persistence.set_omitted_flags(
                event_info.slug, omitted_indices
            )

            pb_index = solve_stats.pb_single_index(
                updated_solves, self._persistence.get_user_pb_single_ms(event_info.slug)
            )
            updated_solves = self._persistence.set_pb_single_flag(event_info.slug, pb_index)

            self._persistence.set_pb_result_flag(
                event_info.slug, self._is_pb_result(event_info.slug, result_ms)
            )

        return EventParticipationRecord(
            status=status,
            solves=updated_solves,
            result_ms=result_ms,
            best_ms=solve_stats.best_time(updated_solves),
            pb_result=self._persistence.get_pb_result_flag(event_info.slug),
        )

    def _validate_submission(self, competition_id: str, event_slug: EventSlug) -> EventInfo:
        """
        Checks that a solve submission references a real event and targets the active
        competition, an event in that competition, and an event the user hasn't already
        finished. Returns the event's info so callers don't need a second lookup.
        """

        active = self._persistence.get_competition()
        if competition_id != active.id:
            raise CompetitionNotActiveException(
                f"Competition '{competition_id}' is not currently active"
            )

        event_info = next(
            (e for e in self._persistence.get_events() if e.slug == event_slug), None
        )
        if event_info is None:
            raise EventNotInCompetitionException(
                f"Event '{event_slug}' is not part of the current competition"
            )

        existing_solves = self._persistence.get_user_solves(event_slug)
        if len(existing_solves) >= event_info.num_solves:
            raise EventAlreadyCompleteException(
                f"Event '{event_slug}' already has a full set of solves"
            )

        return event_info

    def _sorted_events(self, events: list[EventInfo]) -> list[EventInfo]:
        return sorted(events, key=lambda e: SORT_INDEX_BY_EVENT_SLUG[e.slug])


# Swap InMemoryCompetitionPersistence for a DB implementation here when ready
competition_interface = CompetitionInterface(InMemoryCompetitionPersistence())
