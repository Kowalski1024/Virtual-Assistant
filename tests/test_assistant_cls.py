import unittest

from multiprocessing import Pipe, Process
from src.response import ResponseType, Response
from src.core.assistant import Assistant
from unittest import mock


class AssistantTest(unittest.TestCase):
    assistant: Assistant = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.assistant = Assistant()

    def setUp(self) -> None:
        self.parent, self.child = Pipe()
        self.mock = mock.Mock()

    def tearDown(self) -> None:
        self.parent.close()
        self.child.close()

    def test_change_response(self):
        pass
