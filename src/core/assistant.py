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
        if self.process.is_alive():
            self.process.terminate()

        self.process = mp.Process(target=self.obj.run, daemon=True)
        self.process.start()
        return self


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

    def _response(self):
        def response_by_type(d, clear=0):
            if self.response_type:
                self._speaker.response_in_speech(d.message)
            else:
                self._graphical_interface.write(d.message, d.font, clear)

        if self.parent_connection.poll():
            data: Response = self.parent_connection.recv()
            if data.type == ResponseType.WAITING_FOR_SPEECH_INPUT:
                if data.message:
                    response_by_type(data, 2)
                with self._speaker.lock:
                    self._recognizer.obj.lock.release()
                    self._speaker.assistant_ready()
            elif data.type == ResponseType.WAITING_FOR_TEXT_INPUT:
                self._graphical_interface.get_text_input()
            elif data.type in {ResponseType.TEXT_RESPONSE, ResponseType.SPEECH_FAIL, ResponseType.SPEECH_ERROR}:
                print(data)
                response_by_type(data)

        self._graphical_interface.after(ms=20, func=self._response)
