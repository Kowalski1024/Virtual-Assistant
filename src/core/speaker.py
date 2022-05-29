from queue import Queue
from threading import Thread
from os.path import exists

from playsound import playsound
from gtts import gTTS


SOUND_READY = 'files/ready.wav'
SOUND_TEMP = 'files/temp.mp3'

if not exists(SOUND_TEMP):
    with open(SOUND_TEMP, 'x') as f:
        pass


class Speaker:
    def __init__(self):
        self._message_queue = Queue(maxsize=5)
        self._thread = Thread(target=self._run_speech_engine)
        self._stop_speaker = False

    def response_in_speech(self, message):
        self._insert_into_message_queue(message)
        if not self._thread.is_alive():
            self._thread = Thread(target=self._run_speech_engine)
            self._thread.start()

    def _run_speech_engine(self):
        while not self._message_queue.empty():
            message = self._message_queue.get()
            if message:
                batches = self._create_text_batches(raw_text=message)
                for batch in batches:
                    gTTS(batch).save(SOUND_TEMP)
                    playsound(SOUND_TEMP)
                    if self._stop_speaker:
                        self._stop_speaker = False
                        break

    def stop_speaker(self):
        if self._thread.is_alive():
            self._stop_speaker = True
            self._thread.join()

    def _insert_into_message_queue(self, message):
        self._message_queue.put(message)

    @staticmethod
    def assistant_ready():
        playsound(SOUND_READY)

    @staticmethod
    def _create_text_batches(raw_text: str, words_per_batch=8):
        words = raw_text.split(' ')
        for split in range(0, len(words), words_per_batch):
            yield ' '.join(words[split:split + words_per_batch])
