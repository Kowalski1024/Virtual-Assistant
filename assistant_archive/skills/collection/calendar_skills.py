import datetime

from typing import List, Tuple

import dateutil.parser

import win32com.client

from assistant_archive.enumerations import FontStyles
from assistant_archive.response import Connection, ResponseType


class CalendarSkills(Connection):
    def create_event(self) -> None:
        """Creates an event in Outlook calendar"""
        outlook = win32com.client.Dispatch('Outlook.Application')
        event = outlook.CreateItem(1)  # AppointmentItem

        event.Start, event.Subject, event.Duration, event.Location = self._get_event_data()

        if event.Duration == 0:
            return
        
        self.send(ResponseType.TEXT_RESPONSE, f'{event.Start} {event.Subject} {event.Duration} {event.Location}',
                  FontStyles.NORMAL)

        event.Save()
        event.Send()

    def display_events(self) -> None:
        """Gets start and end dates from user.
        Gets events from Outlook Calendar in given range
        """
        outlook = win32com.client.Dispatch('Outlook.Application').GetNamespace('MAPI')
        calender = outlook.GetDefaultFolder(9)
        items = calender.Items

        start_date = self._get_date('Say start date')

        end_date = self._get_date('Say end date')

        select_items = []
        for item in items:
            if start_date <= item.start.date() <= end_date:
                select_items.append(item)

        message = self._create_message(select_items)
        self.send(ResponseType.TEXT_RESPONSE, message, FontStyles.NORMAL)

    def _get_event_data(self) -> Tuple:
        # Gets from user start date, start hour, subject, duration and location of an event
        event_start_date = self._get_date('Say start date: ')
        event_start_hour = self._get_hour('Say start hour: ')
        event_start_date = f'{event_start_date.strftime("%d/%m/%Y")} {event_start_hour}'

        event_subject = self._get_text('Say subject')

        event_duration = self._get_text('Say duration in minutes: ')

        if not event_duration.isnumeric():
            self.send(ResponseType.SKILL_FAIL, 'Duration time is not a number', FontStyles.NORMAL)
            event_duration = 0

        event_location = self._get_text('Say location')

        return event_start_date, event_subject, int(event_duration), event_location

    def _get_date(self, text: str) -> datetime.date:
        # Gets date from user and returns datetime.date object from this date
        while True:
            date_text = self.recv_from_speech(text)
            date = self._convert_to_date(date_text)
            if date:
                break
            self.send(ResponseType.SKILL_FAIL, 'Wrong date', FontStyles.NORMAL)
            
        return date

    def _get_hour(self, text: str) -> str:
        # Gets hour from user and returns hour in specific format
        while True:
            hour_text = self.recv_from_speech(text)
            hour = self._convert_to_hour(hour_text)
            if hour:
                break
            self.send(ResponseType.SKILL_FAIL, 'Wrong hour', FontStyles.NORMAL)

        return hour

    def _get_text(self, text: str) -> str:
        # Gets text from user and removes trailing spaces
        text = self.recv_from_speech(text)
        text = text.strip()
        return text

    @staticmethod
    def _convert_to_date(date_text: str):
        # Converts date from string to datetime.date type
        date_text = date_text.strip()
        try:
            return dateutil.parser.parse(date_text).date()
        except Exception as E:
            return None

    @staticmethod
    def _convert_to_hour(hour_text: str):
        # Converts hour given as string to specific format
        hour_text = hour_text.strip()
        try:
            return f'{dateutil.parser.parse(hour_text).hour}:{dateutil.parser.parse(hour_text).minute}'
        except Exception as e:
            return None


    @staticmethod
    def _create_message(events_items: List) -> str:
        # Creates message from given list of events
        message = ''

        for select_item in events_items:
            message += f'\nSubject: {select_item.subject}\nPlace: {select_item.location}\nStart time: ' \
                       f'{select_item.start}\nEnd time: {select_item.end}\nText: {select_item.body}\n'

        if not message:
            message = 'No events found'

        return message
