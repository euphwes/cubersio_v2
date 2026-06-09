from cubersio.events import ALL_EVENTS
from cubersio.models.competition import Competition, EventInfo, SolveRecord
from cubersio.types import EventSlug

_EVENTS_BY_SLUG = {e.slug: e for e in ALL_EVENTS}


# -----------------------------------------------------------------------------------
# Faux data standing in for a real database. Everything from here down to the class
# definition goes away once a DB-backed persistence implementation exists.
# -----------------------------------------------------------------------------------

_COMPETITION = Competition(
    id="weekly-24-2026",
    name="Weekly Open",
    week_label="Week 24 · Jun 2026",
    week_title="Weekly Open",
)

# Chosen to exercise multiple formats: ao5 (333/222/444/skewb) and mo3 (666)
_COMPETITION_EVENTS: list[EventInfo] = [
    EventInfo(
        slug=slug,
        name=_EVENTS_BY_SLUG[slug].name,
        format=_EVENTS_BY_SLUG[slug].format,
        num_solves=_EVENTS_BY_SLUG[slug].num_solves,
    )
    for slug in EventSlug
]

# The user's personal bests from previous competitions, in ms. Skewb is intentionally
# absent from both, to exercise the no-history path (a first-ever solve/result is
# trivially a PB)
_USER_PB_SINGLE_MS: dict[EventSlug, int] = {
    EventSlug.EVENT_333: 9_840,
    EventSlug.EVENT_222: 2_150,
    EventSlug.EVENT_444: 42_310,
    EventSlug.EVENT_666: 132_450,
}
_USER_PB_RESULT_MS: dict[EventSlug, int] = {
    EventSlug.EVENT_333: 12_470,
    EventSlug.EVENT_222: 3_890,
    EventSlug.EVENT_444: 48_750,
    EventSlug.EVENT_666: 145_620,
}

# One scramble per expected solve: 5 for ao5 events, 3 for mo3 events
_SCRAMBLES: dict[EventSlug, list[str]] = {
    EventSlug.EVENT_333: [
        "R U R' U' R U2 R' F R U R' U' F' R U R' U'",
        "F2 U' B2 D2 L2 F2 U' L2 B2 R' F D' R B U' L U2 F' U'",
        "D2 B2 U2 R2 B2 D R2 U F2 L2 U' F R' U2 B' R2 D F2 R' D2",
        "R2 U' B2 R2 F2 U R2 U' F2 D2 R' F' R2 B U R' U' B' R",
        "U2 R2 B2 D2 B2 R2 U' L2 F2 R2 U' F' R' B R2 B D' L' F2 U",
    ],
    EventSlug.EVENT_222: [
        "R U2 R F2 R' F R2 U' R'",
        "R U' R' U R U2 R' U R' U2 R",
        "U R U2 R' U' R U R' U2",
        "R' U R U2 R' U' R U R' U R",
        "U2 R' U R U2 R U' R' U R",
    ],
    EventSlug.EVENT_444: [
        "Uw2 R2 Fw2 D2 Uw2 R2 Uw2 B2 Uw2 F2 R Uw' F2 D' B Rw U' Fw' Uw' R Uw",
        "Rw2 B2 Uw2 Fw2 D2 Rw2 U' R2 B2 D2 Rw2 D' Rw' U Rw U2 Fw2 Rw' F' Uw'",
        "Fw2 Uw2 R2 B2 Rw2 D Rw2 F2 Rw2 U2 Fw2 R Uw R2 U' Rw' F Rw2 U Fw",
        "Rw2 F2 D2 Rw2 Fw2 U' Rw2 U' F2 Rw2 B2 Rw' D Rw F' Uw' B' Uw2 R' Uw",
        "Uw2 Rw2 F2 Uw2 Fw2 Rw2 F2 R2 B2 U2 R Fw' Rw B2 Uw' F' Uw2 B Rw2 U'",
    ],
    EventSlug.SKEWB: [
        "R' L B' R L' B R' L",
        "B R' L' B R L B' R'",
        "R B L' B' R' L B R",
        "L' B' R L B R' L' B",
        "B' L R' B' L' R B' L",
    ],
    # Scramble strings stay on one line even when long, hence the noqa markers
    EventSlug.EVENT_666: [
        "3Uw2 3Rw2 F2 3Uw2 3Fw2 3Uw2 3Rw2 3Uw2 3Fw2 3Rw2 3Uw Rw F' 3Uw' Rw2 3Fw Rw' 3Uw2 3Fw 3Rw",  # noqa: E501
        "3Rw2 3Uw2 3Fw2 3Rw2 3Uw2 3Fw2 3Rw2 3Fw2 3Uw2 3Rw 3Uw' 3Fw 3Rw' 3Fw' 3Uw 3Rw2 3Fw2 3Rw 3Uw",  # noqa: E501
        "3Fw2 3Rw2 3Uw2 3Fw2 3Rw2 3Uw2 3Fw2 3Rw2 3Uw2 3Fw 3Rw' 3Uw 3Fw' 3Rw 3Uw' 3Fw2 3Rw 3Uw2 3Fw",  # noqa: E501
    ],
}


class InMemoryCompetitionPersistence:
    """
    In-memory stand-in for the eventual DB-backed persistence layer. The current user's
    solves are the only mutable state and live per-process; everything else is served
    from the static faux data above.
    """

    def __init__(self) -> None:
        self._user_solves: dict[EventSlug, list[SolveRecord]] = {}
        # Whether the user's completed result for an event is a PB; written once,
        # when the event's final solve is submitted
        self._user_pb_results: dict[EventSlug, bool] = {}

    def get_competition(self) -> Competition:
        return _COMPETITION

    def get_events(self) -> list[EventInfo]:
        return _COMPETITION_EVENTS

    def get_scrambles(self) -> dict[EventSlug, list[str]]:
        return _SCRAMBLES

    def get_user_solves(self, event_slug: EventSlug) -> list[SolveRecord]:
        return self._user_solves.get(event_slug, [])

    def get_user_pb_single_ms(self, event_slug: EventSlug) -> int | None:
        """
        The user's fastest single for this event from previous competitions, or None
        if they have no recorded history. Excludes the current competition's solves.
        """
        return _USER_PB_SINGLE_MS.get(event_slug)

    def get_user_pb_result_ms(self, event_slug: EventSlug) -> int | None:
        """
        The user's best format result (average/mean/best single) for this event from
        previous competitions, or None if they have no recorded history.
        """
        return _USER_PB_RESULT_MS.get(event_slug)

    def add_solve(self, event_slug: EventSlug, record: SolveRecord) -> list[SolveRecord]:
        solves = self._user_solves.setdefault(event_slug, [])
        solves.append(record)
        return solves

    def set_pb_single_flag(
        self, event_slug: EventSlug, pb_index: int | None
    ) -> list[SolveRecord]:
        """
        Persists which of the user's solves for an event, if any, is their PB single.
        At most one solve is flagged; None flags nothing. Called once, when the final
        solve for an event is submitted.
        """
        solves = self._user_solves.get(event_slug, [])
        for i, solve in enumerate(solves):
            solve.pb_single = i == pb_index
        return solves

    def get_pb_result_flag(self, event_slug: EventSlug) -> bool:
        return self._user_pb_results.get(event_slug, False)

    def set_pb_result_flag(self, event_slug: EventSlug, pb_result: bool) -> None:
        """
        Persists whether the user's completed result for an event beats their best
        from previous competitions. Called once, when the final solve is submitted.
        """
        self._user_pb_results[event_slug] = pb_result

    def set_omitted_flags(
        self, event_slug: EventSlug, omitted_indices: list[int]
    ) -> list[SolveRecord]:
        """
        Persists which of the user's solves are excluded from the event average.
        Called once, when the final solve for an event is submitted.
        """
        solves = self._user_solves.get(event_slug, [])
        for i, solve in enumerate(solves):
            solve.omitted_from_average = i in omitted_indices
        return solves
