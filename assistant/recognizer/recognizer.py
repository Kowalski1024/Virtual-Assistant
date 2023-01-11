from loguru import logger

from assistant.recognizer.recognizers.recognizer_base import RecognizerBase
from assistant.singleton import Singleton


class Recognizer(metaclass=Singleton):
    def __init__(self):
        self._recognizer: RecognizerBase | None = None

    def set_recognizer(self, recognizer: RecognizerBase):
        self._recognizer = recognizer

    def transcribe(self, audio=None) -> str:
        if audio is None:
            logger.info("Start listening...")
            audio = self._microphone()
            logger.info("Listening completed")
        return self._recognizer.transcribe(audio)

    def _microphone(self):
        return self._recognizer.microphone()

