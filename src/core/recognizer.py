import speech_recognition as sr
from multiprocessing import connection

from src.response import Connection, ResponseType


class Recognizer(Connection):
    def __init__(self, pipe: connection):
        super().__init__(pipe)

    def run(self):
        _recognizer = sr.Recognizer()
        text = self._speech_to_text(_recognizer, self._get_input(_recognizer))
        self.send(ResponseType.TEXT_RESPONSE, text)

    @staticmethod
    def _get_input(recognizer: sr.Recognizer) -> sr.AudioData:
        with sr.Microphone() as source:
            audio = recognizer.listen(source)
        return audio

    @staticmethod
    def _speech_to_text(recognizer: sr.Recognizer, audio: sr.AudioData) -> str:
        try:
            text = recognizer.recognize_google(audio_data=audio)
        except sr.UnknownValueError:
            text = "Google Speech Recognition could not understand audio"
        except sr.RequestError as e:
            text = f"Could not request results from Google Speech Recognition service; {e}"
        return text
