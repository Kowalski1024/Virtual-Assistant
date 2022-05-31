import speech_recognition as sr
from multiprocessing import connection, Lock

from src.response import Connection, ResponseType


class Recognizer(Connection):
    def __init__(self, pipe: connection):
        super().__init__(pipe)
        self.lock = Lock()
        self.lock.acquire()
        self._recognizer = sr.Recognizer()

    def run(self):
        while True:
            self.lock.acquire()
            self._speech_to_text(self._get_input())

    def _get_input(self) -> sr.AudioData:
        with sr.Microphone() as source:
            print('ready')
            audio = self._recognizer.listen(source, phrase_time_limit=10)
            print('end')
        return audio

    def _speech_to_text(self, audio: sr.AudioData):
        try:
            text = self._recognizer.recognize_google(audio_data=audio)
            self.send(ResponseType.TEXT_RESPONSE, text)
        except sr.UnknownValueError as e:
            # Google Speech Recognition could not understand audio
            self.send(ResponseType.SPEECH_FAIL, 'Google Speech Recognition could not understand audio')
        except sr.RequestError as e:
            # Could not request results from Google Speech Recognition service
            self.send(ResponseType.SPEECH_ERROR, 'Could not request results from Google Speech Recognition service')
