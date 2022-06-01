import unittest

from src.skills.collection.weather_skills import WeatherSkills
from multiprocessing import Pipe, Process
from src.response import ResponseType, Response


class WeatherTests(unittest.TestCase):
    def setUp(self) -> None:
        self.parent, self.child = Pipe()
        self.weather = WeatherSkills(self.child)
        return super().setUp()

    def test_weather(self):
        process = Process(target=self.weather.run, daemon=True)
        process.start()
        data: Response = self.parent.recv()
        self.assertIs(ResponseType.WAITING_FOR_SPEECH_INPUT, data.type)
        self.parent.send(Response(ResponseType.TEXT_RESPONSE, 'Warsaw'))
        data: Response = self.parent.recv()
        self.assertNotEqual(data.message, 'City not found')


if __name__ == "__main__":
    unittest.main()
