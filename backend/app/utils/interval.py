from datetime import datetime


class Interval:
    def __init__(self, start: datetime, end: datetime):
        self.start = start
        self.end = end

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, start):
        self._start = start

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, end):
        self._end = end

    def is_intersecting(self, other) -> bool:
        """
        Returns True if two intervals are intersecting or if they're "touching" (same start date as end date)
        """
        if (
            self.start.date() == other.end.date()
            or self.end.date() == other.start.date()
        ):
            return True
        return (self.start <= other.start <= self.end) or (
            other.start <= self.start <= other.end
        )
