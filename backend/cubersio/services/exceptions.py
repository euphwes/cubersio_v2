class InvalidSubmissionException(Exception):
    """Base class for solve submissions that are invalid for any reason."""


class CompetitionNotActiveException(InvalidSubmissionException):
    """Raised when a submission targets a competition that is not currently active."""


class EventNotInCompetitionException(InvalidSubmissionException):
    """Raised when a submission targets an event not held in the active competition."""


class EventAlreadyCompleteException(InvalidSubmissionException):
    """Raised when a submission targets an event the user has already finished."""
