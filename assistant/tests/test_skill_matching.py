import unittest

from assistant.skills.skill_matching import SkillMatching
from multiprocessing import Pipe, Process
from assistant.response import ResponseType, Response


class SkillMatchingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.parent, self.child = Pipe()
        self.skill_matching = SkillMatching(self.child)
        self.process = Process(target=self.skill_matching.run, daemon=True)
        self.process.start()

    def tearDown(self) -> None:
        self.process.terminate()
        self.parent.close()
        self.child.close()

    def test_probability_less_than_one(self):
        self.parent.send(Response(ResponseType.TEXT_RESPONSE, 'wiki'))
        self.parent.send(Response(ResponseType.TEXT_RESPONSE, 'no'))
        self.parent.send(Response(ResponseType.TEXT_RESPONSE, 'show wikipedia'))
        self.parent.send(Response(ResponseType.TEXT_RESPONSE, 'yes'))
        self.parent.send(Response(ResponseType.TEXT_RESPONSE, 'Tokyo'))
        data: Response = self.parent.recv()
        self.assertNotEqual(data.type, ResponseType.FAIL_MATCH)

    def test_skill_matching_wikipedia(self):
        self.parent.send(Response(ResponseType.TEXT_RESPONSE, 'wikipedia'))
        data: Response = self.parent.recv()
        self.assertNotEqual(data.type, ResponseType.FAIL_MATCH)

    def test_skill_matching_synonyms(self):
        self.parent.send(Response(ResponseType.TEXT_RESPONSE, 'synonyms'))
        data: Response = self.parent.recv()
        self.assertNotEqual(data.type, ResponseType.FAIL_MATCH)

    def test_skill_matching_search_on_google(self):
        self.parent.send(Response(ResponseType.TEXT_RESPONSE, 'search'))
        data: Response = self.parent.recv()
        self.assertNotEqual(data.type, ResponseType.FAIL_MATCH)

    def test_skill_matching_open_website(self):
        self.parent.send(Response(ResponseType.TEXT_RESPONSE, 'open'))
        data: Response = self.parent.recv()
        self.assertNotEqual(data.type, ResponseType.FAIL_MATCH)

    def test_skill_matching_reminder(self):
        self.parent.send(Response(ResponseType.TEXT_RESPONSE, 'reminder'))
        data: Response = self.parent.recv()
        self.assertNotEqual(data.type, ResponseType.FAIL_MATCH)


if __name__ == "__main__":
    unittest.main()
