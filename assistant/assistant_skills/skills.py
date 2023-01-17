import asyncio
from typing import Iterator
import webbrowser
import requests
import datetime

import win32com.client
import pythoncom
import wikipedia
import python_weather


from assistant.handlers import *
from assistant.observable import ObservableDict
from assistant.singleton import Singleton
from assistant.model.reminder import ReminderModel


class Skills(metaclass=Singleton):
    @staticmethod
    def _iterate(chain, data):
        for description, function in HandlerDescriptionIterator(chain):
            yield description

            while True:
                try:
                    data = function(data)
                except ValueError as e:
                    yield f'{e}\n{description}'
                else:
                    break

        yield 'Finished'

    def create_event_in_calendar(self, data: ObservableDict) -> Iterator[str]:
        chain = [
            DateHandler(),
            ClockTimeHandler(),
            DurationHandler(),
            TextHandler(key='subject', description='Give event subject', optional=False),
            TextHandler(key='location', description='Specify location', optional=True)
        ]

        yield from self._iterate(chain, data)

        date = data['date'].strftime("%d/%m/%Y")
        clock_time = f"{data['hour']}:{data['minute']}"

        event_start = f'{date} {clock_time}'

        outlook = win32com.client.Dispatch('Outlook.Application', pythoncom.CoInitialize())
        event = outlook.CreateItem(1)
        event.Start = event_start
        event.Subject = data['subject']
        event.Duration = data['duration']
        event.Location = data['location']

        event.Save()
        event.Send()

    def display_event_in_calendar(self, data: ObservableDict) -> Iterator[str]:
        chain = [
            DateHandler(key='start'),
            DateHandler(key='end'),
        ]

        yield from self._iterate(chain, data)

        outlook = win32com.client.Dispatch('Outlook.Application', pythoncom.CoInitialize()).GetNamespace('MAPI')
        calender = outlook.GetDefaultFolder(9)
        items = calender.Items

        message = ''

        for item in items:
            if data['start'] <= item.start.date() <= data['end']:
                message += f'\nSubject: {item.subject}\nPlace: {item.location}\nStart time: ' \
                           f'{item.start}\nEnd time: {item.end}\nText: {item.body}\n'

        if not message:
            message = 'No events found'

        data['events'] = message

    def google_search(self, data: ObservableDict) -> Iterator[str]:
        chain = [
            TextHandler(key='keyword', description='Say keyword', optional=False)
        ]

        yield from self._iterate(chain, data)

        keyword = data["keyword"]

        webbrowser.open_new_tab(f'https://www.google.com/search?q={keyword.replace(" ", "+")}')

    def wikipedia(self, data: ObservableDict) -> Iterator[str]:
        chain = [
            TextHandler(key='keyword', description='Say keyword', optional=False)
        ]

        yield from self._iterate(chain, data)

        keyword = data["keyword"]

        try:
            page = wikipedia.page(keyword)
            data["title"] = page.title
            data["summary"] = page.summary
        except wikipedia.WikipediaException:
            yield 'Cannot find given keyword'

    def synonyms(self, data: ObservableDict) -> Iterator[str]:
        chain = [
            TextHandler(key='word', description='Say word', optional=False)
        ]

        yield from self._iterate(chain, data)

        word = data["word"]

        url = f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}'
        response = requests.get(url).json()

        result = []
        no_of_words = len(response)

        # We iterate through the whole API response, because synonyms can be in different places
        for q in range(no_of_words):
            no_of_meanings = len(response[q]['meanings'])
            for i in range(no_of_meanings):
                for synonym in response[q]['meanings'][i]['synonyms']:
                    result.append(synonym)

                no_of_definitions = len(response[q]['meanings'][i]['definitions'])
                for j in range(no_of_definitions):
                    for synonym in response[q]['meanings'][i]['definitions'][j]['synonyms']:
                        result.append(synonym)

        result = sorted(set(result))
        data['results'] = ', '.join(result)

    def weather(self, data: ObservableDict) -> Iterator[str]:
        async def get_weather(loc):
            async with python_weather.Client(format=python_weather.METRIC) as client:
                _weather = await client.get(loc)
                return _weather

        chain = [
            TextHandler(key='city', description='Say city', optional=False)
        ]

        yield from self._iterate(chain, data)

        city = data["city"]

        weather = asyncio.run(get_weather(city))

        print(weather)

        message = f'\n{weather.location}\nNow: {str(weather.current.temperature)} C ' \
                  f'{weather.current.description}\n'

        for forecast in weather.forecasts:
            date = datetime.date(forecast.date.year, forecast.date.month, forecast.date.day)
            if date >= datetime.date.today():
                message += 'Today' if date == datetime.date.today() else date.strftime("%d/%m/%Y")
                message += f': {str(forecast.temperature)} C\n'

        data['results'] = message

    def create_reminder(self, data: ObservableDict) -> Iterator[str]:
        chain = [
            DurationHandler()
        ]

        yield from self._iterate(chain, data)

        duration = data['duration']
        reminder = ReminderModel.from_duration(minutes=duration, message='xd')
        print(reminder)
        reminder.save()



