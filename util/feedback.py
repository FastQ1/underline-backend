"""
Handlers for feedback operations.
"""
from config.db import get_database, get_database_client_name
from models import exceptions
import models.events as event_models
import models.feedback as feedback_models


# instanciate the main collection to use for this util file for convenience
def feedback_collection():
    return get_database()[get_database_client_name()]["feedback"]


def events_collection():
    return get_database()[get_database_client_name()]["events"]


async def delete_feedback(event_id: event_models.EventId,
                          feedback_id: feedback_models.FeedbackId) -> None:
    """
    Given an event id and feedback id, attempt to delete the feedback from
    the event's comment_ids array as well as from the feedback collection
    """
    found_event = events_collection().find_one({"_id": event_id})

    if not found_event:
        raise exceptions.EventNotFoundException

    if feedback_id not in found_event["comment_ids"]:
        raise exceptions.FeedbackNotFoundException

    # remove the feedback ID from the event then update the DB document to match
    found_event["comment_ids"].remove(feedback_id)
    events_collection().update_one({"_id": event_id}, {"$set": found_event})

    # remove feedback from the feedback collection
    feedback_collection().delete_one({"_id": feedback_id})


async def register_feedback(
    registration_form: feedback_models.FeedbackRegistrationRequest
) -> feedback_models.FeedbackId:
    """
    Given an event id, create a feedback id and add the feedback to the event
    """
    # attempt to find given event
    event_id = registration_form.event_id
    found_event = events_collection().find_one({"_id": event_id})
    if not found_event:
        raise exceptions.EventNotFoundException

    # add feedback id to event and update it in the database
    feedback_id = registration_form.get_id()
    found_event["comment_ids"].append(feedback_id)
    events_collection().update_one({"_id": event_id}, {"$set": found_event})

    # finally, insert the feedback into the feedback collection
    feedback_collection().insert_one(registration_form.dict())

    return feedback_id


async def get_feedback(
        feedback_id: feedback_models.FeedbackId) -> feedback_models.Feedback:
    """
    Returns the feedback document as a Feedback object given it's id.
    """
    feedback = feedback_collection().find_one({"_id": feedback_id})

    if not feedback:
        raise exceptions.FeedbackNotFoundException

    return feedback_models.Feedback(**feedback)
