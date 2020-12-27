from datetime import datetime


def datetime_without_seconds(date: datetime) -> datetime:
    """
    Returns given datetime with seconds and microseconds set to 0
    """
    return date.replace(second=0, microsecond=0)
