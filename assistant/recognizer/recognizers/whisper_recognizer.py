import io
from tempfile import NamedTemporaryFile

import whisper
from speech_recognition import AudioData
from whisper.normalizers import EnglishTextNormalizer

from assistant.recognizer.recognizers.recognizer_base import RecognizerBase


class WhisperRecognizer(RecognizerBase):
    def __init__(self):
        super().__init__()
        self.model = whisper.load_model('base.en', in_memory=False)
        self.normalizer = EnglishTextNormalizer()
        self.temp_file = NamedTemporaryFile().name

    def transcribe(self, audio):
        if isinstance(audio, AudioData):
            audio = self._to_ndarray(audio)
        text = self.model.transcribe(audio)['text']
        return self.normalizer(text)

    def _to_ndarray(self, audio: AudioData) -> str:
        wav_data = io.BytesIO(audio.get_wav_data())
        with open(self.temp_file, 'w+b') as f:
            f.write(wav_data.read())

        return self.temp_file

    def __str__(self):
        return "Whisper"
