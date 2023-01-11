import speech_recognition as sr


class RecognizerBase:
    def __init__(self):
        self._sr = sr.Recognizer()

    def microphone(self) -> str:
        with sr.Microphone() as source:
            audio = self._sr.listen(source, phrase_time_limit=10)
        return audio

    def transcribe(self, audio):
        raise NotImplementedError
