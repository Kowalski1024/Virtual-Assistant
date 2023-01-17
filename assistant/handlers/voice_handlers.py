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
    def __init__(self, key: str = 'date', description='Specify date'):
        super().__init__(key, description=description)

    def handle(self, request: MutableMapping) -> MutableMapping:
        logger.info('Waiting for input...')

        text = self._recognizer.transcribe()
        text = f' {text} '.replace(' one ', '1')

        try:
            request[self._key] = dateutil.parser.parse(text.strip()).date()
        except dateutil.parser.ParserError:
            raise ValueError(f"Can't parse {text}")

        return request


class ClockTimeHandler(VoiceHandlerBase):
    def __init__(self, description='Specify the clock time'):
        super().__init__(description=description)

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


class DurationHandler(VoiceHandlerBase):
    def __init__(self, description='Specify duration in hours or/and minutes'):
        super().__init__(description=description)

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


class TextHandler(VoiceHandlerBase):
    def __init__(self, key='text', description='Say something', optional=False):
        super().__init__(key, description)
        self._desc = description if not optional else f'{description} or say pass to skip'
        self._optional = optional

    def handle(self, request: MutableMapping) -> MutableMapping:
        logger.info('Waiting for input')

        text = self._recognizer.transcribe()

        if self._optional and text == 'pass':
            request[self._key] = ''
            return request

        request[self._key] = text

        return request
