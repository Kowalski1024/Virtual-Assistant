import unittest
from unittest import mock
from pynput import keyboard

from assistant.skills.collection.browser_skills import BrowserSkills
from multiprocessing import Pipe, Process
from assistant.response import ResponseType, Response


def test_startup(key_listener_asset, method):
    process = Process(target=method, daemon=True)
    process.start()
    data: Response = key_listener_asset.parent.recv()
    key_listener_asset.assertIs(ResponseType.WAITING_FOR_SPEECH_INPUT, data.type)


class InternetTests(unittest.TestCase):
    def setUp(self) -> None:
        self.parent, self.child = Pipe()
        self.internet_cls = BrowserSkills(self.child)
        return super().setUp()

    def test_wikipedia(self):
        test_startup(self, self.internet_cls.wikipedia)
        self.parent.send(Response(ResponseType.TEXT_RESPONSE, 'Tokyo'))
        data: Response = self.parent.recv()
        self.assertEqual('Tokyo', data.message)

    def test_google_search(self):
        test_startup(self, self.internet_cls.search_on_google)
        self.parent.send(Response(ResponseType.TEXT_RESPONSE, 'Tokyo'))
        data: Response = self.parent.recv()
        self.assertEqual('Phrase searched', data.message)

    def test_open_website_in_browser(self):
        test_startup(self, self.internet_cls.open_website_in_browser)
        self.parent.send(Response(ResponseType.TEXT_RESPONSE, 'youtube'))
        data: Response = self.parent.recv()
        self.assertEqual('Browser opened', data.message)

    def test_synonym_search(self):
        test_startup(self, self.internet_cls.show_synonyms)
        self.parent.send(Response(ResponseType.TEXT_RESPONSE, 'yes'))
        synonyms = "['agree', 'aye', 'consent', 'nod', 'yea', 'affirmative', 'all right']"
        data: Response = self.parent.recv()
        self.assertTrue(all(x in synonyms for x in data.message), "Couldn't find synonyms")


if __name__ == "__main__":
    unittest.main()
