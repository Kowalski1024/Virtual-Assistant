from datetime import datetime
import re


import win32com.client


class CalendarModel:
    def __init__(self):
        self._date = None
        self._time = None
        self._duration = None
        self._subject = ''
        self._location = ''

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value: datetime.date):
        self._date = value

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value: tuple[int, int]):
        if not 0 <= value[0] <= 24:
            raise ValueError("Wrong hour value")
        if not 0 <= value[1] <= 60:
            raise ValueError("Wrong minutes value")

        self._time = value

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, value: int):
        if value <= 0:
            raise ValueError("Duration should be longer than 0 minutes")

        self._duration = value

    @property
    def subject(self):
        return self._subject

    @subject.setter
    def subject(self, value: str):
        self._subject = value

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value: str):
        self._location = value

    # @classmethod
    # def get_events(cls, start, end):
    #     calender = cls.CLIENT.GetDefaultFolder(9)
    #     items = calender.Items
    #
    #     events = []
    #
    #     for item in items:
    #         if start <= item.start.date() <= end:
    #             event = {
    #                 'subject': item.subject,
    #                 'place': item.location,
    #                 'start': item.start,
    #                 'end': item.end,
    #                 'description': item.body
    #             }
    #
    #             events.append(event)
    #
    #     return events
