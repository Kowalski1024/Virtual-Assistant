import unittest

from multiprocessing import Pipe, Process
from src.response import ResponseType, Response
from src.core.assistant import Assistant
from unittest import mock


class AssistantTest(unittest.TestCase):
    assistant: Assistant = None

    def _send(self, response_type, message):
        self.child.send(Response(response_type, message))

    @classmethod
    def setUpClass(cls) -> None:
        cls.assistant = Assistant()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.assistant._graphical_interface.on_quit()

    def setUp(self) -> None:
        self.parent, self.child = self.assistant.pipe
        self.mock = mock.Mock()

    def test_change_response(self):
        self.assertEqual(self.assistant.response_type, False)
        self._send(ResponseType.CHANGE_RESPONSE, 'voice')
        self.assistant._response()
        self.assertEqual(self.assistant.response_type, True)
        self._send(ResponseType.CHANGE_RESPONSE, 'text')
        self.assistant._response()
        self.assertEqual(self.assistant.response_type, False)

    def test_wake_up(self):
        self.assertEqual(self.assistant._skill_matching.process.is_alive(), False)
        self.assistant.wake_up()
        self.assertEqual(self.assistant._skill_matching.process.is_alive(), True)
        self.assistant.wake_up()
        self.assertEqual(self.assistant._skill_matching.process.is_alive(), False)

