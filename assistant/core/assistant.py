import multiprocessing as mp

from .key_listener import KeyListener
from .recognizer import Recognizer
from .speaker import Speaker
from ..gui import GUI
from ..skills.skill_matching import SkillMatching
from assistant.response import Response, ResponseType
from assistant.enumerations import FontStyles


class ProcessTuple:
    def __init__(self, obj):
        if not hasattr(obj, 'run'):
            raise NotImplementedError('Object does not have \"run\" attribute')
        self.obj = obj
        self.process = mp.Process()

    def run(self) -> 'ProcessTuple':
        """
        Terminate process if is alive and create new process
        """
        self.terminate()

        self.process = mp.Process(target=self.obj.run, daemon=True)
        self.process.start()
        return self

    def is_alive(self) -> bool:
        """
        Check if process is alive
        """
        return self.process.is_alive()

    def terminate(self) -> None:
        """
        Terminate process if is alive
        """
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

    def run(self) -> None:
        """
        Head function to run the assistant, starts all necessary threads and enters an infinite loop to manage the gui
        """
        self._key_listener.start()
        self._graphical_interface.after(ms=20, func=self._response)
        self._graphical_interface.run()
        self._key_listener.stop()
        self._speaker.stop_speaker()
        self.close_connection()

    def wake_up(self) -> None:
        """
        Start the skills matching process if there is an internet connection (otherwise a message will be displayed)
        and the last process is not active.
        If the last process is alive, the function will terminate only that process.
        """
        from assistant.skills.collection.browser_skills import BrowserSkills

        self._graphical_interface.clear()
        if self._speaker.speaker_alive():
            self._speaker.stop_speaker()
        else:
            if self._skill_matching.is_alive():
                self._skill_matching.terminate()
            else:
                if BrowserSkills.internet_connectivity_check():
                    self._skill_matching.run()
                else:
                    self._graphical_interface.write('Sorry, no internet connection', FontStyles.TITLE, clear=2)

    @property
    def parent_connection(self) -> mp.connection:
        """
        Return pipe connection on the parent side for communication with another process
        """
        return self._pipe_connection[0]

    @property
    def child_connection(self) -> mp.connection:
        """
        Return pipe connection on the child side for communication with another process
        """
        return self._pipe_connection[1]

    @property
    def pipe(self) -> mp.connection:
        """
        Return duplex pipe connection for communication with another process
        """
        return self._pipe_connection

    def close_connection(self) -> None:
        """
        Close pipe connection
        """
        self._pipe_connection[0].close()
        self._pipe_connection[1].close()

    def _response_by_type(self, response, clear=0) -> None:
        # Create an audio or graphic response for user, depends on user preference
        if self.response_type:
            self._speaker.response_in_speech(response.message)
        else:
            self._graphical_interface.write(response.message, response.font, clear)

    def _get_speech_input(self, response: Response) -> None:
        # Release lock from recognizer to get speech input from user,
        # if there is a message to the user, it will be passed on to him
        if response.message:
            self._response_by_type(response, 2)
        with self._speaker.lock:
            try:
                self._recognizer.obj.lock.release()
            except ValueError:
                return
            self._speaker.assistant_ready()

    def _change_response_type(self, response) -> None:
        # Change response type to graphic or audio
        if response.message == 'voice':
            self.response_type = True
        else:
            self.response_type = False

    def _response(self) -> None:
        # Process all data from pipe connection, every 20ms
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
            elif response.type in {ResponseType.SPEECH_FAIL, ResponseType.SPEECH_ERROR, ResponseType.FAIL_MATCH}:
                self._response_by_type(response, clear=2)

        self._graphical_interface.after(ms=20, func=self._response)
