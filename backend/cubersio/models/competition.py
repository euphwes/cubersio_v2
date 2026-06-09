from abc import ABC

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from cubersio.types import EventFormat, EventSlug, ParticipationStatus


class BaseCubersioModel(BaseModel, ABC):
    # Serialize snake_case fields as camelCase to match frontend Typescript conventions
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class SolveRecord(BaseCubersioModel):
    """A single solve by a user within an event during a competition."""

    # Elapsed time of the solve, measured in milliseconds. Is null for DNFs that
    # because the user's inspection time expired past the -2s threshold.
    time_ms: int | None
    # Whether the solve is a DNF (did not finish).
    dnf: bool
    # Whether the solve carries a +2s penalty.
    plus_two: bool
    # Whether this solve is excluded from the average (parenthesized in standard
    # results notation). False until the event's final solve is submitted, at which
    # point the flags are computed once and persisted with the solves.
    # TODO do these need defaults?
    omitted_from_average: bool = False
    # True on at most one solve per event: the fastest successful solve of the set,
    # when it beats the user's PB single from previous competitions. Evaluated and
    # persisted once, when the event's final solve is submitted; False until then.
    # DNFs are never PBs.
    pb_single: bool = False


class EventParticipationRecord(BaseCubersioModel):
    """A user's overall participation in one event in one competition.

    Tracks their status for that event, lists the individual solves,
    and contains their overall result; single, mean, and/or average,
    depending on the event format.
    """

    status: ParticipationStatus
    solves: list[SolveRecord]
    # Backend-computed stats. result_ms is the format-appropriate result (average/mean
    # for ao5/mo3, best single for best-of formats; None while incomplete or DNF).
    # best_ms is redundant with result_ms for best-of formats, but kept as a tiebreaker
    # between tied averages/means
    result_ms: int | None
    best_ms: int | None
    # True once the event is complete and result_ms beats the user's best result for
    # this event from previous competitions
    pb_result: bool


class EventInfo(BaseCubersioModel):
    """Static details of one event within a competition.

    Identity and display info only; nothing user-specific lives here.
    """

    slug: EventSlug
    name: str
    format: EventFormat
    # How many solves make a full set for this event; follows from the format
    # (5 for ao5/bo5, 3 for mo3/bo3, 1 for bo1)
    num_solves: int


class Competition(BaseCubersioModel):
    """Identity and display details of a single weekly competition.

    Not an API model on its own; the persistence layer serves these fields,
    and WeeklyCompetitionRecord extends them into the full page payload.
    """

    id: str
    name: str
    week_label: str
    week_title: str


class WeeklyCompetitionRecord(Competition):
    """Everything the compete page needs to render, in a single payload.

    Extends the competition's identity and display fields with its events,
    the user's participation so far in each event, and the scrambles for
    each event.
    """

    # In display order
    events: list[EventInfo]
    user_participation: dict[EventSlug, EventParticipationRecord]
    # One scramble per expected solve for each event, keyed by event slug
    scrambles: dict[EventSlug, list[str]]


class SolveInput(BaseCubersioModel):
    """A single solve as submitted by the frontend; raw time and penalties only.

    Stats and PB flags are computed and persisted on the backend,
    not accepted from the client.
    """

    time_ms: int | None
    dnf: bool = False
    plus_two: bool = False
