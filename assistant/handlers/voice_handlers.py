from typing import MutableMapping
import re

from loguru import logger
import dateutil.parser

from assistant.handlers.handler_base import VoiceHandlerBase


__all__ = [
    'DateHandler',
    'ClockTimeHandler',
    'DurationHandler',
    'TextHandler',
]


class DateHandler(VoiceHandlerBase):
    def handle(self, request: MutableMapping) -> MutableMapping:
        logger.info('Waiting for input...')

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
    def handle(self, request: MutableMapping) -> MutableMapping:
        logger.info('Waiting for input')

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
    def handle(self, request: MutableMapping) -> MutableMapping:
        logger.info('Waiting for input')

        text = self._recognizer.transcribe()
        text = f' {text} '.replace(' one ', '1')

        try:
            hours, minutes = re.findall(r'([0-9]+) hour?|([0-9]+) minute?', text)[0]

            hours = int(hours) if hours else 0
            minutes = int(minutes) if minutes else 0

        except (ValueError, IndexError):
            raise ValueError(f"Can't parse {text}")

        duration_minutes = hours * 60 + minutes

        if duration_minutes <= 0:
            raise ValueError("Duration mustn't be zero")

        request['duration'] = duration_minutes

        return request

    @property
    def description(self):
        return 'Specify duration in hours or/and minutes'


class TextHandler(VoiceHandlerBase):
    def __init__(self, name='text', description='Say something', optional=False):
        self._name = name
        self._desc = description if not optional else f'{description} or say pass to skip'
        self._optional = optional

    def handle(self, request: MutableMapping) -> MutableMapping:
        logger.info('Waiting for input')

        text = self._recognizer.transcribe()

        if self._optional and text == 'pass':
            request[self._name] = ''
            return request

        request[self._name] = text

        return request

    @property
    def description(self):
        return self._desc
