import tkinter as tk
import multiprocessing as mp
import threading as th

from .key_listener import KeyListener
from .recognizer import Recognizer
from .speaker import Speaker
from ..gui import GUI
from ..skills.skill_matching import SkillMatching
from src.response import Response, ResponseType


class Assistant:
    def __init__(self):
        self._key_listener = KeyListener(self.wake_up)
        self._pipe_connection = mp.Pipe()
        self._speech_process_lock = mp.Lock()
        self._speaker_lock = th.Lock()
        self._recognizer = Recognizer(self.parent_connection, self._speech_process_lock)
        self._speaker = Speaker(self._speaker_lock)
        self._skill_matching = SkillMatching(self.child_connection)
        self._skill_matching_process = mp.Process()
        self._speech_recognizer_process = mp.Process(target=self._recognizer.run, daemon=True)
        self._graphical_interface = GUI(self.parent_connection)
        self._response_type = False

        self._speech_process_lock.acquire()
        self._speech_recognizer_process.start()

    def run(self):
        self._key_listener.start()
        self._graphical_interface.after(ms=20, func=self._response)
        self._graphical_interface.run()
        self._key_listener.stop()
        self.close_connection()

    def wake_up(self):
        if self._skill_matching_process.is_alive():
            self._skill_matching_process.terminate()
        else:
            self._skill_matching_process = mp.Process(target=self._skill_matching.run,
                                                   daemon=True)
            self._skill_matching_process.start()

    @property
    def parent_connection(self) -> mp.connection:
        return self._pipe_connection[0]

    @property
    def child_connection(self) -> mp.connection:
        return self._pipe_connection[1]

    @property
    def pipe(self):
        return self._pipe_connection

    def close_connection(self):
        self._pipe_connection[0].close()
        self._pipe_connection[1].close()

    def _response(self):
        def response_by_type(d):
            if self._response_type:
                self._speaker.response_in_speech(d.message)
            else:
                self._graphical_interface.write(d.message, d.font)

        if self.parent_connection.poll():
            data: Response = self.parent_connection.recv()
            if data.type == ResponseType.WAITING_FOR_SPEECH_INPUT:
                with self._speaker_lock:
                    self._speech_process_lock.release()
                    self._speaker.assistant_ready()
            # elif data.type == ResponseType.FAIL_MATCH:
            #     print(data.message, data.type)
            elif data.type in {ResponseType.TEXT_RESPONSE, ResponseType.SPEECH_FAIL, ResponseType.SPEECH_ERROR}:
                print(data)
                response_by_type(data)
                # self._graphical_interface.write(data.message, data.font)

        self._graphical_interface.after(ms=20, func=self._response)
