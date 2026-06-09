from cubersio.models.competition import SolveRecord
from cubersio.types import EventFormat

# DNFs are given a sentinel value larger than any real solve time so they sort as "worst"
_DNF_SENTINEL = 10_000_000

# A +2 penalty adds two seconds to the recorded time
_PLUS_TWO_PENALTY_MS = 2000


def effective_time(solve: SolveRecord) -> int:
    """The solve's counting time: the recorded time plus any +2 penalty."""
    return (solve.time_ms or 0) + (_PLUS_TWO_PENALTY_MS if solve.plus_two else 0)


def result_for_format(solves: list[SolveRecord], event_format: EventFormat) -> int | None:
    """
    The result appropriate to the event's format: avg-of-5 for ao5, mean for mo3, and
    the best single for best-of formats (bo1/bo3/bo5), which rank by single time.
    None means no result: an incomplete or DNF average/mean, or no successful solve.
    """
    if event_format is EventFormat.AVERAGE_OF_FIVE:
        return avg_of_five(solves)
    if event_format is EventFormat.MEAN_OF_THREE:
        return mean_of_three(solves)
    return best_time(solves)


def pb_single_index(solves: list[SolveRecord], prior_pb_ms: int | None) -> int | None:
    """
    Index of the solve that holds the event's PB single flag: the fastest successful
    solve of the set, provided it beats the user's PB single from previous
    competitions (or the user has none). Returns None when no solve qualifies.
    DNFs are never PBs, and ties don't count as new PBs; a tie within the set goes
    to the earliest solve.
    """
    candidates = [
        (effective_time(s), i)
        for i, s in enumerate(solves)
        if not s.dnf and s.time_ms is not None
    ]
    if not candidates:
        return None

    best_ms, best_idx = min(candidates)
    if prior_pb_ms is not None and best_ms >= prior_pb_ms:
        return None
    return best_idx


def omitted_solve_indices(solves: list[SolveRecord], event_format: EventFormat) -> list[int]:
    """
    Indices of the solves excluded from the average, i.e. the parenthesized solves in
    standard results notation: best and worst of a complete ao5, nothing for other
    formats or incomplete sets. DNFs count as worst, and ties are broken by position so
    exactly one best and one worst are returned.
    """
    if event_format is not EventFormat.AVERAGE_OF_FIVE or len(solves) < 5:
        return []

    times = [_DNF_SENTINEL if s.dnf else effective_time(s) for s in solves]
    best_idx = min(range(len(times)), key=lambda i: (times[i], i))
    worst_idx = max(range(len(times)), key=lambda i: (times[i], i))
    return [best_idx, worst_idx]


def avg_of_five(solves: list[SolveRecord]) -> int | None:
    """
    WCA avg-of-5: drop best and worst, average the middle 3.
    Returns None if fewer than 5 solves or if 2+ are DNFs.
    """
    if len(solves) < 5:
        return None

    dnf_count = sum(1 for s in solves if s.dnf)
    if dnf_count >= 2:
        return None

    times = [_DNF_SENTINEL if s.dnf else effective_time(s) for s in solves]
    times.sort()
    return sum(times[1:4]) // 3


def mean_of_three(solves: list[SolveRecord]) -> int | None:
    """
    WCA mean-of-3: straight average of all 3 solves.
    Returns None if fewer than 3 solves or if any solve is a DNF.
    """
    if len(solves) < 3:
        return None

    if any(s.dnf for s in solves):
        return None

    return sum(effective_time(s) for s in solves) // 3


def best_time(solves: list[SolveRecord]) -> int | None:
    # The +2 penalty counts toward the single's time, so compare effective times
    valid = [effective_time(s) for s in solves if not s.dnf and s.time_ms is not None]
    return min(valid) if valid else None
