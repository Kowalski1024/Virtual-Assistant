from multiprocessing import Process, Lock, Queue
import os

from playsound import playsound
from gtts import gTTS


SOUND_READY = 'files/ready.wav'
SOUND_TEMP = 'files/temp.mp3'


class Speaker:
    def __init__(self):
        self.lock = Lock()
        self._queue = Queue(maxsize=5)
        self._process = Process()
        self._stop_speaker = False

    def response_in_speech(self, message):
        self._insert_into_message_queue(message)
        if not self.speaker_alive():
            self._process = Process(target=self._run_speech_engine, args=(self._queue, ), daemon=True)
            self._process.start()

    @staticmethod
    def _run_speech_engine(queue: Queue):
        def _create_text_batches(raw_text: str, words_per_batch=16):
            words = raw_text.split(' ')
            for split in range(0, len(words), words_per_batch):
                yield ' '.join(words[split:split + words_per_batch])

        while not queue.empty():
            message = queue.get()
            if message:
                batches = _create_text_batches(raw_text=message)
                for batch in batches:
                    with open(SOUND_TEMP, 'xb') as f:
                        gTTS(batch).write_to_fp(f)
                    playsound(SOUND_TEMP)
                    os.remove(SOUND_TEMP)

    def stop_speaker(self):
        if self.speaker_alive():
            self._process.terminate()
            while not self._queue.empty():
                self._queue.get()
            if os.path.exists(SOUND_TEMP):
                os.remove(SOUND_TEMP)

    def speaker_alive(self):
        return self._process.is_alive()

    def _insert_into_message_queue(self, message):
        self._queue.put(message)

    @staticmethod
    def assistant_ready():
        playsound(SOUND_READY)
