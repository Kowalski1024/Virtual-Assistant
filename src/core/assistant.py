import tkinter as tk
from multiprocessing import Process, Pipe, connection

from .key_listener import KeyListener
from .recognizer import Recognizer
from ..gui import GUI
from ..skills.skill_matching import SkillMatching
from src.response import Response, ResponseType


class Assistant:
    def __init__(self):
        self._key_listener = KeyListener(self.wake_up)
        self._pipe_connection = Pipe()
        self._recognizer = Recognizer(self.parent_connection)
        self._skill_matching = SkillMatching(self.child_connection)
        self._skill_matching_process = Process()
        self._speech_recognizer_process = Process()
        self._graphical_interface = GUI(self.parent_connection)

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
            self._skill_matching_process = Process(target=self._skill_matching.run,
                                                   args=(self.child_connection,),
                                                   daemon=True)
            self._skill_matching_process.start()

    def _run_recognizer(self):
        if not self._speech_recognizer_process.is_alive():
            self._speech_recognizer_process = Process(target=self._recognizer.run,
                                                      args=(self.parent_connection,),
                                                      daemon=True)
            self._speech_recognizer_process.start()

    @property
    def parent_connection(self) -> connection:
        return self._pipe_connection[0]

    @property
    def child_connection(self) -> connection:
        return self._pipe_connection[1]

    def close_connection(self):
        self._pipe_connection[0].close()
        self._pipe_connection[1].close()

    def _response(self):
        pass
