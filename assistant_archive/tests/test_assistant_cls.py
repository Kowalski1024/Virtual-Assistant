import unittest

from multiprocessing import Pipe, Process
from assistant_archive.response import ResponseType, Response
from assistant_archive.core.assistant import Assistant
from unittest import mock


def internet_connectivity_check(url='http://www.google.com/', timeout=2):
    import requests
    """
        Checks for internet connection availability based on google page.
    """
    try:
        _ = requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        return False


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
        self._send(ResponseType.CHANGE_RESPONSE, 'recognizer')
        self.assistant._response()
        self.assertEqual(self.assistant.response_type, True)
        self._send(ResponseType.CHANGE_RESPONSE, 'text')
        self.assistant._response()
        self.assertEqual(self.assistant.response_type, False)

    def test_wake_up(self):
        self.assertEqual(self.assistant._skill_matching.process.is_alive(), False)
        self.assistant.wake_up()
        if internet_connectivity_check():
            self.assertEqual(self.assistant._skill_matching.process.is_alive(), True)
        else:
            self.assertEqual(self.assistant._skill_matching.process.is_alive(), False)
        self.assistant.wake_up()
        self.assertEqual(self.assistant._skill_matching.process.is_alive(), False)

