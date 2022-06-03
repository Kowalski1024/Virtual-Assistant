import unittest
from assistant.skills.collection.weather_skills import WeatherSkills
from multiprocessing import Pipe, Process
from assistant.response import ResponseType, Response

days = ['Now', 'Today', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
conditions = ['rain', 'sun', 'cloud', 'storm', 'clear', 'hurricane', 'snow', 'tornado', 'wind']


def test(weather_skills, str_to_check):
    process = Process(target=weather_skills.weather.run, daemon=True)
    process.start()
    data: Response = weather_skills.parent.recv()
    weather_skills.assertIs(ResponseType.WAITING_FOR_SPEECH_INPUT, data.type)
    weather_skills.parent.send(Response(ResponseType.TEXT_RESPONSE, str_to_check))
    data: Response = weather_skills.parent.recv()
    msg_lower = data.message.lower()
    str_to_check = str_to_check.lower()
    weather_skills.assertEqual(msg_lower[:data.message.index(',')], str_to_check)
    result = data.message.splitlines()
    i = 0
    for string in result:
        if i == 0:
            i = 1
            continue

        day = string[:string.index(':')]
        weather_skills.assertIn(day, days)
        temperature = string[string.index(' ') + 1:string.index('C') - 1]
        weather_skills.assertTrue(temperature.isdigit(), f'{temperature} is not a number')
        weather_cond = string[string.index('C') + 1:].lower()
        flag = False

        for condition in conditions:
            if condition in weather_cond:
                flag = True

        weather_skills.assertTrue(flag, f'{weather_cond} is not a weather condition')
        process.terminate()


class WeatherTests(unittest.TestCase):
    def setUp(self) -> None:
        self.parent, self.child = Pipe()
        self.weather = WeatherSkills(self.child)
        return super().setUp()

    def tearDown(self) -> None:
        self.parent.close()
        self.child.close()

    def test_weather2(self):
        test(self, 'Oslo')

    def test_weather1(self):
        test(self, 'Cracow')

    def test_weather3(self):
        process = Process(target=self.weather.run, daemon=True)
        process.start()
        data: Response = self.parent.recv()
        self.assertIs(ResponseType.WAITING_FOR_SPEECH_INPUT, data.type)
        self.parent.send(Response(ResponseType.TEXT_RESPONSE, ''))
        data: Response = self.parent.recv()
        self.assertEqual(data.message, 'City not found')
        process.terminate()

    def test_weather4(self):
        test(self, 'new york')


if __name__ == "__main__":
    unittest.main()
