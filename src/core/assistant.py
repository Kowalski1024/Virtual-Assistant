import multiprocessing as mp

from .key_listener import KeyListener
from .recognizer import Recognizer
from .speaker import Speaker
from ..gui import GUI
from ..skills.skill_matching import SkillMatching
from src.response import Response, ResponseType


class ProcessTuple:
    def __init__(self, obj):
        if not hasattr(obj, 'run'):
            raise NotImplementedError('Object does not have \"run\" attribute')
        self.obj = obj
        self.process = mp.Process()

    def run(self):
        self.terminate()

        self.process = mp.Process(target=self.obj.run, daemon=True)
        self.process.start()
        return self

    def is_alive(self):
        return self.process.is_alive()

    def terminate(self):
        if self.is_alive():
            self.process.terminate()
            self.process.join()


class Assistant:
    def __init__(self):
        self._key_listener = KeyListener(self.wake_up)
        self._pipe_connection = mp.Pipe()
        self._speaker = Speaker()
        self._skill_matching = ProcessTuple(SkillMatching(self.child_connection))
        self._recognizer = ProcessTuple(Recognizer(self.parent_connection)).run()
        self._graphical_interface = GUI(self.parent_connection)
        self.response_type = False

    def run(self):
        self._key_listener.start()
        self._graphical_interface.after(ms=20, func=self._response)
        self._graphical_interface.run()
        self._key_listener.stop()
        self._speaker.stop_speaker()
        self.close_connection()

    def wake_up(self):
        self._graphical_interface.clear()
        if self._speaker.speaker_alive():
            self._speaker.stop_speaker()
        else:
            if self._skill_matching.is_alive():
                self._skill_matching.terminate()
            else:
                self._skill_matching.run()

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

    def _response_by_type(self, response, clear=0):
        if self.response_type:
            self._speaker.response_in_speech(response.message)
        else:
            self._graphical_interface.write(response.message, response.font, clear)

    def _get_speech_input(self, response: Response):
        if response.message:
            self._response_by_type(response, 2)
        with self._speaker.lock:
            try:
                self._recognizer.obj.lock.release()
            except ValueError:
                return
            self._speaker.assistant_ready()

    def _change_response_type(self, response):
        if response.message == 'voice':
            self.response_type = True
        else:
            self.response_type = False

    def _response(self):
        if self.parent_connection.poll():
            response: Response = self.parent_connection.recv()
            if response.type == ResponseType.WAITING_FOR_SPEECH_INPUT:
                self._get_speech_input(response)
            elif response.type == ResponseType.WAITING_FOR_TEXT_INPUT:
                self._graphical_interface.get_text_input()
            elif response.type == ResponseType.CHANGE_RESPONSE:
                self._change_response_type(response)
            elif response.type == ResponseType.TEXT_RESPONSE:
                self._response_by_type(response)
            elif response.type in {ResponseType.SPEECH_FAIL, ResponseType.SPEECH_ERROR}:
                self._response_by_type(response, clear=2)

        self._graphical_interface.after(ms=20, func=self._response)
