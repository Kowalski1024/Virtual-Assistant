import datetime

import win32com.client

from src.enumerations import FontStyles
from src.response import ResponseType, Connection


class CalendarSkills(Connection):
    @staticmethod
    def create_event():
        raise NotImplementedError

    def display_events(self):
        outlook = win32com.client.Dispatch('Outlook.Application').GetNamespace('MAPI')
        calender = outlook.GetDefaultFolder(9)
        items = calender.Items

        self.send(ResponseType.TEXT_RESPONSE, 'Enter start date: ', FontStyles.NORMAL)
        start_date = self._get_date()

        self.send(ResponseType.TEXT_RESPONSE, 'Enter end date: ', FontStyles.NORMAL)
        end_date = self._get_date()

        select_items = []
        for item in items:
            if start_date <= item.start.date() <= end_date:
                select_items.append(item)

        message = self._format_message(items)
        self.send(ResponseType.TEXT_RESPONSE, message, FontStyles.NORMAL)

    def _get_date(self):
        date = self.recv_from_speech()
        date = self._convert_to_date(date)

        return date

    @staticmethod
    def _convert_to_date(date_text, date_format='%d %B %Y'):
        date_text = date_text.strip()
        return datetime.datetime.strptime(date_text, date_format).date()

    @staticmethod
    def _format_message(items):
        message = ''

        for select_item in items:
            message += f'\nSubject: {select_item.subject}\nPlace: {select_item.location}\nStart time: ' \
                       f'{select_item.start}\nEnd time: {select_item.end}\nText: {select_item.body}\n'

        return message



