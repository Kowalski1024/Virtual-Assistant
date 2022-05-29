import speech_recognition as sr
from multiprocessing import connection, Lock

from src.response import Connection, ResponseType


class Recognizer(Connection):
    def __init__(self, pipe: connection, lock: Lock):
        super().__init__(pipe)
        self._lock = lock
        self._recognizer = sr.Recognizer()

    def run(self):
        while True:
            self._lock.acquire()
            self._speech_to_text(self._get_input())

    def _get_input(self) -> sr.AudioData:
        with sr.Microphone() as source:
            print('ready')
            try:
                audio = self._recognizer.listen(source, timeout=1)
            except sr.WaitTimeoutError:
                print('timeout')
            print('end')
        return audio

    def _speech_to_text(self, audio: sr.AudioData):
        try:
            text = self._recognizer.recognize_google(audio_data=audio)
            self.send(ResponseType.TEXT_RESPONSE, text)
        except sr.UnknownValueError as e:
            # Google Speech Recognition could not understand audio
            self.send(ResponseType.SPEECH_FAIL, str(e))
        except sr.RequestError as e:
            # Could not request results from Google Speech Recognition service
            self.send(ResponseType.SPEECH_ERROR, str(e))
