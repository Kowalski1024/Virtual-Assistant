import unittest
from assistant.skills.collection.weather_skills import WeatherSkills
from multiprocessing import Pipe, Process
from assistant.response import ResponseType, Response

days = ['Now', 'Today', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
conditions = ['rain', 'sun', 'cloud', 'storm', 'clear', 'hurricane', 'snow', 'tornado', 'wind']


class WeatherTests(unittest.TestCase):
    def setUp(self) -> None:
        self.parent, self.child = Pipe()
        self.weather = WeatherSkills(self.child)
        return super().setUp()

    def tearDown(self) -> None:
        self.parent.close()
        self.child.close()

    def test_weather(self):
        process = Process(target=self.weather.run, daemon=True)
        process.start()
        data: Response = self.parent.recv()
        self.assertIs(ResponseType.WAITING_FOR_SPEECH_INPUT, data.type)
        self.parent.send(Response(ResponseType.TEXT_RESPONSE, 'Oslo'))
        data: Response = self.parent.recv()
        self.assertEqual(data.message[:data.message.index(',')], 'Oslo')
        result = data.message.splitlines()
        i = 0
        for string in result:
            if i == 0:
                i = 1
                continue

            day = string[:string.index(':')]
            self.assertIn(day, days)
            temperature = string[string.index(' ') + 1:string.index('C') - 1]
            self.assertTrue(temperature.isdigit(), f'{temperature} is not a number')
            weather_cond = string[string.index('C') + 1:].lower()
            flag = False

            for condition in conditions:
                if condition in weather_cond:
                    flag = True

            self.assertTrue(flag, f'{weather_cond} is not a weather condition')


if __name__ == "__main__":
    unittest.main()
