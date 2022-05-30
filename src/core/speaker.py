from queue import Queue
from threading import Thread, Lock
import os

from playsound import playsound
from gtts import gTTS


SOUND_READY = 'files/ready.wav'
SOUND_TEMP = 'files/temp.mp3'


if os.path.exists(SOUND_TEMP):
    os.remove(SOUND_TEMP)


class Speaker:
    def __init__(self):
        self.lock = Lock()
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
                with self.lock:
                    batches = self._create_text_batches(raw_text=message)
                    for batch in batches:
                        with open(SOUND_TEMP, 'xb') as f:
                            gTTS(batch).write_to_fp(f)
                        playsound(SOUND_TEMP)
                        if self._stop_speaker:
                            self._stop_speaker = False
                            break
                        os.remove(SOUND_TEMP)

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
    def _create_text_batches(raw_text: str, words_per_batch=16):
        words = raw_text.split(' ')
        for split in range(0, len(words), words_per_batch):
            yield ' '.join(words[split:split + words_per_batch])
