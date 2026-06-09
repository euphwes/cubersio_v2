from dataclasses import dataclass

from cubersio.types import EventCategory, EventFormat, EventSlug


@dataclass(frozen=True)
class EventDefinition:
    name: str
    slug: EventSlug
    format: EventFormat
    # Number of solves a participant completes for this event; must agree with format
    num_solves: int
    category: EventCategory


# Source of truth set of all events supported by cubers.io.
ALL_EVENTS = frozenset(
    [
        EventDefinition(
            name="3x3",
            slug=EventSlug.EVENT_333,
            format=EventFormat.AVERAGE_OF_FIVE,
            num_solves=5,
            category=EventCategory.WCA,
        ),
        EventDefinition(
            name="2x2",
            slug=EventSlug.EVENT_222,
            format=EventFormat.AVERAGE_OF_FIVE,
            num_solves=5,
            category=EventCategory.WCA,
        ),
        EventDefinition(
            name="4x4",
            slug=EventSlug.EVENT_444,
            format=EventFormat.AVERAGE_OF_FIVE,
            num_solves=5,
            category=EventCategory.WCA,
        ),
        EventDefinition(
            name="5x5",
            slug=EventSlug.EVENT_555,
            format=EventFormat.AVERAGE_OF_FIVE,
            num_solves=5,
            category=EventCategory.WCA,
        ),
        EventDefinition(
            name="6x6",
            slug=EventSlug.EVENT_666,
            format=EventFormat.MEAN_OF_THREE,
            num_solves=3,
            category=EventCategory.WCA,
        ),
        EventDefinition(
            name="7x7",
            slug=EventSlug.EVENT_777,
            format=EventFormat.MEAN_OF_THREE,
            num_solves=3,
            category=EventCategory.WCA,
        ),
        EventDefinition(
            name="3x3 Blindfolded",
            slug=EventSlug.EVENT_3BLD,
            format=EventFormat.BEST_OF_FIVE,
            num_solves=5,
            category=EventCategory.WCA,
        ),
        EventDefinition(
            name="4x4 Blindfolded",
            slug=EventSlug.EVENT_4BLD,
            format=EventFormat.BEST_OF_THREE,
            num_solves=3,
            category=EventCategory.WCA,
        ),
        EventDefinition(
            name="5x5 Blindfolded",
            slug=EventSlug.EVENT_5BLD,
            format=EventFormat.BEST_OF_THREE,
            num_solves=3,
            category=EventCategory.WCA,
        ),
        EventDefinition(
            name="3x3 Multi-Blind",
            slug=EventSlug.MBLD,
            format=EventFormat.BEST_OF_ONE,
            num_solves=1,
            category=EventCategory.WCA,
        ),
        EventDefinition(
            name="3x3 One-Handed",
            slug=EventSlug.EVENT_3OH,
            format=EventFormat.AVERAGE_OF_FIVE,
            num_solves=5,
            category=EventCategory.WCA,
        ),
        EventDefinition(
            name="3x3 Fewest Moves",
            slug=EventSlug.FMC,
            format=EventFormat.MEAN_OF_THREE,
            num_solves=3,
            category=EventCategory.WCA,
        ),
        EventDefinition(
            name="Square-1",
            slug=EventSlug.SQ1,
            format=EventFormat.AVERAGE_OF_FIVE,
            num_solves=5,
            category=EventCategory.WCA,
        ),
        EventDefinition(
            name="Pyraminx",
            slug=EventSlug.PYRA,
            format=EventFormat.AVERAGE_OF_FIVE,
            num_solves=5,
            category=EventCategory.WCA,
        ),
        EventDefinition(
            name="Megaminx",
            slug=EventSlug.MEGA,
            format=EventFormat.AVERAGE_OF_FIVE,
            num_solves=5,
            category=EventCategory.WCA,
        ),
        EventDefinition(
            name="Skewb",
            slug=EventSlug.SKEWB,
            format=EventFormat.AVERAGE_OF_FIVE,
            num_solves=5,
            category=EventCategory.WCA,
        ),
        EventDefinition(
            name="Clock",
            slug=EventSlug.CLOCK,
            format=EventFormat.AVERAGE_OF_FIVE,
            num_solves=5,
            category=EventCategory.WCA,
        ),
        EventDefinition(
            name="FTO",
            slug=EventSlug.FTO,
            format=EventFormat.AVERAGE_OF_FIVE,
            num_solves=5,
            category=EventCategory.BONUS,
        ),
        EventDefinition(
            name="3x3 Mirror Cube",
            slug=EventSlug.MIRROR,
            format=EventFormat.AVERAGE_OF_FIVE,
            num_solves=5,
            category=EventCategory.BONUS,
        ),
        EventDefinition(
            name="Redi Cube",
            slug=EventSlug.REDI,
            format=EventFormat.AVERAGE_OF_FIVE,
            num_solves=5,
            category=EventCategory.BONUS,
        ),
        EventDefinition(
            name="15 Puzzle",
            slug=EventSlug.FIFTEEN,
            format=EventFormat.AVERAGE_OF_FIVE,
            num_solves=5,
            category=EventCategory.BONUS,
        ),
    ]
)


_GLOBAL_SORT_ORDER = [
    # NxN events
    EventSlug.EVENT_333,
    EventSlug.EVENT_222,
    EventSlug.EVENT_444,
    EventSlug.EVENT_555,
    EventSlug.EVENT_666,
    EventSlug.EVENT_777,
    # Other WCA events
    EventSlug.SKEWB,
    EventSlug.PYRA,
    EventSlug.MEGA,
    EventSlug.SQ1,
    EventSlug.CLOCK,
    EventSlug.FMC,
    EventSlug.EVENT_3OH,
    # Blindfolded
    EventSlug.EVENT_3BLD,
    EventSlug.EVENT_4BLD,
    EventSlug.EVENT_5BLD,
    EventSlug.MBLD,
    # Bonus
    EventSlug.FTO,
    EventSlug.REDI,
    EventSlug.FIFTEEN,
    EventSlug.MIRROR,
]

SORT_INDEX_BY_EVENT_SLUG = {slug: i for i, slug in enumerate(_GLOBAL_SORT_ORDER)}
