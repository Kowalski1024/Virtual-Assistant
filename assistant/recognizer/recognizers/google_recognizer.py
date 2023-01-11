from assistant.recognizer.recognizers.recognizer_base import RecognizerBase


class GoogleRecognizer(RecognizerBase):
    def transcribe(self, audio):
        return self._sr.recognize_google(audio_data=audio)
