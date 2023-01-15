import speech_recognition as sr

from assistant.recognizer.recognizers.recognizer_base import RecognizerBase


class GoogleRecognizer(RecognizerBase):
    def transcribe(self, audio):
        try:
            return self._sr.recognize_google(audio_data=audio)
        except sr.UnknownValueError:
            raise ValueError("Lack of voice")

    def __str__(self):
        return "GoogleAPI"
