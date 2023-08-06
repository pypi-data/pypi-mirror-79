import datetime


def log_level_as_severity(logger, name: str, event_dict: dict) -> dict:
    """
    Adds logging level to `event_dict` as `severity` field
    """
    event_dict["severity"] = event_dict.pop("level", "info")
    return event_dict


def log_event_as_message(logger, name: str, event_dict: dict) -> dict:
    """
    Renames `event` field to `message`
    """
    event = event_dict.pop("event", None)
    if event:
        event_dict["message"] = event
    return event_dict


def log_timestamp_rfc3339(logger, name: str, event_dict: dict) -> dict:
    """
    Add timestamp into `event_dict` in RFC3339
    """
    event_dict["timestamp"] = datetime.datetime.utcnow().isoformat("T") + "Z"
    return event_dict
