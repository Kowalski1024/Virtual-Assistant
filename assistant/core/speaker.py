from multiprocessing import Process, Lock, Queue
import os

from playsound import playsound
from gtts import gTTS

SOUND_READY = 'assistant/files/ready.wav'
SOUND_TEMP = 'assistant/files/temp.mp3'


class Speaker:
    def __init__(self):
        self.lock = Lock()
        self._queue = Queue(maxsize=5)
        self._process = Process()
        self._stop_speaker = False

    def response_in_speech(self, message) -> None:
        """
        Add message to queue and if the process responsible for the sound is dead, it will be restarted
        """
        self._insert_into_message_queue(message)
        if not self.speaker_alive():
            self._process = Process(target=self._run_speech_engine, args=(self._queue,), daemon=True)
            self._process.start()

    def stop_speaker(self) -> None:
        """
        Terminate the process if it is alive, clear the message queue
        and delete the temporary mp3 file created by this process
        """
        if self.speaker_alive():
            self._process.terminate()
            while not self._queue.empty():
                self._queue.get()
            if os.path.exists(SOUND_TEMP):
                os.remove(SOUND_TEMP)

    def speaker_alive(self) -> bool:
        """
        Check if process is alive
        """
        return self._process.is_alive()

    def _insert_into_message_queue(self, message):
        # Add message to queue
        self._queue.put(message)

    @staticmethod
    def assistant_ready() -> None:
        # plays assistant ready sound
        playsound(SOUND_READY)

    @staticmethod
    def _run_speech_engine(queue: Queue) -> None:
        # Converting text from queue to speech, save as temp mp3 file and plays the audio
        def _create_text_batches(raw_text: str, words_per_batch=16) -> list[str]:
            # divides the text into batches
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
