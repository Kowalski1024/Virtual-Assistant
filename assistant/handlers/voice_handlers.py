import re

import dateutil.parser

from assistant.handlers.handler_base import VoiceHandlerBase


class DateHandler(VoiceHandlerBase):
    def handle(self, request: dict) -> dict:
        text = self._recognizer.transcribe()
        text = f' {text} '.replace(' one ', '1')

        try:
            request['date'] = dateutil.parser.parse(text.strip()).date()
        except dateutil.parser.ParserError:
            raise ValueError(f"Can't parse {text}")

        return request

    @property
    def description(self):
        return 'Specify date'


class ClockTimeHandler(VoiceHandlerBase):
    def handle(self, request: dict) -> dict:
        text = self._recognizer.transcribe()
        text = f' {text} '.replace(' one ', '1')

        try:
            request['hour'] = dateutil.parser.parse(text.strip()).hour
            request['minute'] = dateutil.parser.parse(text.strip()).minute
        except dateutil.parser.ParserError:
            raise ValueError(f"Can't parse {text}")

        return request

    @property
    def description(self):
        return 'Specify the clock time'


class DurationHandler(VoiceHandlerBase):
    def handle(self, request: dict) -> dict:
        text = self._recognizer.transcribe()
        text = f' {text} '.replace(' one ', '1')

        try:
            hours, minutes = re.findall(r'([0-9]+) hour?|([0-9]+) minute?', text)[0]

            hours = int(hours) if hours else 0
            minutes = int(minutes) if minutes else 0
            request['duration'] = hours*60 + minutes

        except (ValueError, IndexError):
            raise ValueError(f"Can't parse {text}")

        return request

    @property
    def description(self):
        return 'Specify duration in hours or/and minutes'


class LocationHandler(VoiceHandlerBase):
    def handle(self, request: dict) -> dict:
        text = self._recognizer.transcribe()

        if text != 'pass':
            request['location'] = text

        return request

    @property
    def description(self):
        return 'Specify location or say pass to skip'


class TextHandler(VoiceHandlerBase):
    def __init__(self, description=None):
        self._desc = description if description else 'Say something'

    def handle(self, request: dict) -> dict:
        text = self._recognizer.transcribe()

        if text != 'pass':
            request['text'] = text

        return request

    @property
    def description(self):
        return self._desc


class OptionalTextHandler(VoiceHandlerBase):
    def handle(self, request: dict) -> dict:
        text = self._recognizer.transcribe()

        if text != 'pass':
            request['text'] = text

        return request

    @property
    def description(self):
        return 'Say something or say pass to skip'



