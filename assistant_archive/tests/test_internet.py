import unittest
from unittest import mock
from pynput import keyboard

from assistant_archive.skills.collection.browser_skills import BrowserSkills
from multiprocessing import Pipe, Process
from assistant_archive.response import ResponseType, Response
from assistant_archive.tests.test_assistant_cls import internet_connectivity_check


class InternetTests(unittest.TestCase):
    def setUp(self) -> None:
        self.parent, self.child = Pipe()
        self.internet_cls = BrowserSkills(self.child)
        return super().setUp()

    def tearDown(self) -> None:
        self.parent.close()
        self.child.close()

    def test_wikipedia(self):
        self.assertTrue(internet_connectivity_check(), 'No internet connection')

        process = Process(target=self.internet_cls.wikipedia, daemon=True)
        process.start()
        data: Response = self.parent.recv()
        self.assertIs(ResponseType.WAITING_FOR_SPEECH_INPUT, data.type)

        self.parent.send(Response(ResponseType.TEXT_RESPONSE, 'Tokyo'))
        data: Response = self.parent.recv()
        self.assertEqual('Tokyo', data.message)
        process.terminate()

    def test_wikipedia_cannot_find_keyword(self):
        self.assertTrue(internet_connectivity_check(), 'No internet connection')

        process = Process(target=self.internet_cls.wikipedia, daemon=True)
        process.start()
        data: Response = self.parent.recv()
        self.assertIs(ResponseType.WAITING_FOR_SPEECH_INPUT, data.type)

        self.parent.send(Response(ResponseType.TEXT_RESPONSE, ''))
        data: Response = self.parent.recv()
        self.assertEqual('Cannot find given keyword', data.message)
        process.terminate()

    def test_google_search(self):
        self.assertTrue(internet_connectivity_check(), 'No internet connection')

        process = Process(target=self.internet_cls.search_on_google, daemon=True)
        process.start()
        data: Response = self.parent.recv()
        self.assertIs(ResponseType.WAITING_FOR_SPEECH_INPUT, data.type)

        self.parent.send(Response(ResponseType.TEXT_RESPONSE, 'Tokyo'))
        data: Response = self.parent.recv()
        self.assertEqual('Phrase searched', data.message)
        process.terminate()


    def test_open_website_in_browser(self):
        self.assertTrue(internet_connectivity_check(), 'No internet connection')

        process = Process(target=self.internet_cls.open_website_in_browser, daemon=True)
        process.start()
        data: Response = self.parent.recv()
        self.assertIs(ResponseType.WAITING_FOR_SPEECH_INPUT, data.type)

        self.parent.send(Response(ResponseType.TEXT_RESPONSE, 'youtube'))
        data: Response = self.parent.recv()
        self.assertEqual('Browser opened', data.message)
        process.terminate()

    def test_no_website_given(self):
        self.assertTrue(internet_connectivity_check(), 'No internet connection')

        process = Process(target=self.internet_cls.open_website_in_browser, daemon=True)
        process.start()
        data: Response = self.parent.recv()
        self.assertIs(ResponseType.WAITING_FOR_SPEECH_INPUT, data.type)

        self.parent.send(Response(ResponseType.TEXT_RESPONSE, ''))
        data: Response = self.parent.recv()
        self.assertEqual('Cannot open the website', data.message)
        process.terminate()

    def test_synonym_search(self):
        self.assertTrue(internet_connectivity_check(), 'No internet connection')

        process = Process(target=self.internet_cls.show_synonyms, daemon=True)
        process.start()
        data: Response = self.parent.recv()
        self.assertIs(ResponseType.WAITING_FOR_SPEECH_INPUT, data.type)

        self.parent.send(Response(ResponseType.TEXT_RESPONSE, 'yes'))
        synonyms = "['agree', 'aye', 'consent', 'nod', 'yea', 'affirmative', 'all right']"
        data: Response = self.parent.recv()
        self.assertTrue(all(x in synonyms for x in data.message), "Couldn't find synonyms")
        process.terminate()

    def test_synonym_search_empty(self):
        self.assertTrue(internet_connectivity_check(), 'No internet connection')

        process = Process(target=self.internet_cls.show_synonyms, daemon=True)
        process.start()
        data: Response = self.parent.recv()
        self.assertIs(ResponseType.WAITING_FOR_SPEECH_INPUT, data.type)

        self.parent.send(Response(ResponseType.TEXT_RESPONSE, ''))
        data: Response = self.parent.recv()
        self.assertTrue(data.message, "Couldn't find synonyms")
        process.terminate()


if __name__ == "__main__":
    unittest.main()
