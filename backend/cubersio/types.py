from enum import StrEnum


class EventSlug(StrEnum):
    """Short URL-safe identifiers for every event the site supports."""

    EVENT_333 = "333"
    EVENT_222 = "222"
    EVENT_444 = "444"
    EVENT_555 = "555"
    EVENT_666 = "666"
    EVENT_777 = "777"
    FMC = "fmc"
    EVENT_3OH = "3oh"
    EVENT_3BLD = "3bld"
    EVENT_4BLD = "4bld"
    EVENT_5BLD = "5bld"
    SQ1 = "sq1"
    SKEWB = "skewb"
    MBLD = "mbld"
    PYRA = "pyra"
    MEGA = "mega"
    CLOCK = "clock"
    FTO = "fto"
    MIRROR = "mirror"
    REDI = "redi"
    FIFTEEN = "15puzzle"


class ParticipationStatus(StrEnum):
    """A user's progress through a single event's solves."""

    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETE = "complete"


class EventCategory(StrEnum):
    """Whether an event is an official WCA event or a site-specific bonus event."""

    WCA = "wca"
    BONUS = "bonus"


class EventFormat(StrEnum):
    """How an event's overall result is computed from its solves.

    Average formats drop the best and worst solves and average the rest;
    mean formats average all solves; best-of formats take the fastest single.
    """

    AVERAGE_OF_FIVE = "ao5"
    BEST_OF_FIVE = "bo5"
    MEAN_OF_THREE = "mo3"
    BEST_OF_THREE = "bo3"
    BEST_OF_ONE = "bo1"
