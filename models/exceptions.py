# pylint: disable=unsubscriptable-object
#       - pylint bug with optional
"""
Holds all of the common exceptions that get re-raised as HTTPExceptions.

Should all come with a pre-set message that can be overriden.
"""

from typing import Optional
from starlette.exceptions import HTTPException


class EventNotFoundException(HTTPException):
    """
    Default exception for a 404 on events.
    """
    def __init__(self, detail: Optional[str] = None):
        if not detail:
            detail = "Event not found with given ID"
        super().__init__(status_code=404, detail=detail)


class UserNotFoundException(HTTPException):
    """
    Default exception for a 404 on users.
    """
    def __init__(self, detail: Optional[str] = None):
        if not detail:
            detail = "User not found with given identifier"
        super().__init__(status_code=404, detail=detail)


class FeedbackNotFoundException(HTTPException):
    """
    Default exception for a 404 on a feedback per event.
    """
    def __init__(self, detail: Optional[str] = None):
        if not detail:
            detail = "Feedback ID not found in the provided event"
        super().__init__(status_code=404, detail=detail)


class InvalidDataException(HTTPException):
    """
    Default for invalid entry data that raises a 422
    """
    def __init__(self, detail: Optional[str] = None):
        if not detail:
            detail = "Invalid data provided"
        super().__init__(status_code=422, detail=detail)
