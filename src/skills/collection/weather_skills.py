import asyncio
import datetime

import python_weather

from src.enumerations import FontStyles
from src.response import Connection, ResponseType


class WeatherSkills(Connection):
    def run(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.check_weather())

    async def check_weather(self):
        client = python_weather.Client()
        city = self.recv_from_speech()

        if city not in (ResponseType.SPEECH_FAIL, ResponseType.SPEECH_ERROR):
            try:
                weather = await client.find(city)
            except Exception as e:
                self.send(ResponseType.SKILL_FAIL, 'City not found', FontStyles.NORMAL)
                await client.close()

            message = self._format_message(weather)
            self.send(ResponseType.TEXT_RESPONSE, message, FontStyles.NORMAL)
        else:
            self.send(ResponseType.SKILL_FAIL, 'City not found', FontStyles.NORMAL)

        await client.close()

    @staticmethod
    def _format_message(weather, temperature_unit='C'):
        message = f'{weather.location_name}\nNow: {str(weather.current.temperature)} {temperature_unit} ' \
                  f'{weather.current.sky_text}\n'

        for forecast in weather.forecasts:
            date = datetime.date(forecast.date.year, forecast.date.month, forecast.date.day)
            if date >= datetime.date.today():
                message += 'Today' if date == datetime.date.today() else forecast.day
                message += f': {str(forecast.temperature)} {temperature_unit} {forecast.sky_text}\n'

        return message
