import speech_recognition as sr
from multiprocessing import connection

from src.response import Connection, ResponseType


class Recognizer(Connection):
    def __init__(self, pipe: connection):
        super().__init__(pipe)
        self._recognizer = sr.Recognizer()

    def run(self):
        self._speech_to_text(self._get_input())

    def _get_input(self) -> sr.AudioData:
        with sr.Microphone() as source:
            audio = self._recognizer.listen(source)
        return audio

    def _speech_to_text(self, audio: sr.AudioData):
        try:
            text = self._recognizer.recognize_google(audio_data=audio)
            self.send(ResponseType.TEXT_RESPONSE, text)
        except sr.UnknownValueError:
            # Google Speech Recognition could not understand audio
            self.send(ResponseType.SPEECH_FAIL)
        except sr.RequestError as e:
            # Could not request results from Google Speech Recognition service
            self.send(ResponseType.SPEECH_ERROR, str(e))
