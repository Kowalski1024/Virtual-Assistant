from typing import Iterator

import win32com.client
import pythoncom

from assistant.handlers import *
from assistant.observable import ObservableDict
from assistant.singleton import Singleton


class Skills(metaclass=Singleton):
    def __init__(self):
        self._date_handler = DateHandler()
        self._clock_time_handler = ClockTimeHandler()
        self._duration_handler = DurationHandler()

    def create_event_in_calendar(self, data: ObservableDict) -> Iterator[str]:
        chain = [
            self._date_handler,
            self._clock_time_handler,
            self._duration_handler,
            TextHandler(name='subject', description='Give event subject', optional=False),
            TextHandler(name='location', description='Specify location', optional=True)

        ]

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
