from datetime import datetime


def datetime_without_seconds(date: datetime) -> datetime:
    return date.replace(second=0, microsecond=0)
