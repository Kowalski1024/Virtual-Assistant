import tkinter as tk
from multiprocessing import Process, Pipe, connection

from .key_listener import KeyListener
from .recognizer import Recognizer
from ..gui import GUI
from ..skills import SkillMatching
from src.response import Response, ResponseType


class Assistant:
    def __init__(self):
        self._key_listener = KeyListener(self.wake_up)
        self._pipe_connection = Pipe()
        self._skill_matching = SkillMatching(self.child_connection)
        self.skill_matching_process = Process(target=self._skill_matching.run,
                                              args=(self.child_connection,),
                                              daemon=True)

    def run(self):
        raise NotImplementedError

    def wake_up(self):
        if self.skill_matching_process.is_alive():
            self.skill_matching_process.terminate()
        else:
            self.skill_matching_process = Process(target=self._skill_matching.run,
                                                  args=(self.child_connection,),
                                                  daemon=True)
            self.skill_matching_process.start()

    @property
    def parent_connection(self) -> connection:
        return self._pipe_connection[0]

    @property
    def child_connection(self) -> connection:
        return self._pipe_connection[1]

    def _response(self):
        raise NotImplementedError
