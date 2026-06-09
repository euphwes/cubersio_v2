from fastapi import APIRouter, HTTPException

from cubersio.models.competition import (
    EventParticipationRecord,
    SolveInput,
    WeeklyCompetitionRecord,
)
from cubersio.services.competition import competition_interface
from cubersio.services.exceptions import InvalidSubmissionException
from cubersio.types import EventSlug

router = APIRouter(prefix="/competition")


@router.get("/current", response_model=WeeklyCompetitionRecord)
async def get_current_competition() -> WeeklyCompetitionRecord:
    """Returns a summary of the active competition.

    WeeklyCompetitionRecord includes, at a high level:
    - name of the competition
    - list of events within the competition
    - scrambles for each event
    - a record of the user's participation in each event
        - status (unstarted, in-progress, complete)
        - record of solves so far
    """

    return competition_interface.get_competition_page()


@router.post(
    "/{competition_id}/events/{event_slug}/solve",
    response_model=EventParticipationRecord,
)
async def submit_solve(
    competition_id: str,
    event_slug: EventSlug,
    solve: SolveInput,
) -> EventParticipationRecord:
    """Accepts a solve submission for the specified competition and event.

    Returns a record of the user's current participation in this event.
    """

    try:
        return competition_interface.submit_solve(competition_id, event_slug, solve)
    except InvalidSubmissionException as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
