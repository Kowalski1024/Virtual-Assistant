import re
import time

from threading import Thread
from typing import Tuple

from assistant.enumerations import FontStyles
from assistant.response import ResponseType, Connection, Response

time_intervals = {
    'seconds': {'variations': ['sec', 'second', 'seconds', 'Sec', 'Second', 'Seconds'],
                'scheduler_interval': 's'
                },
    'minutes': {'variations': ['minute', 'minutes', 'Minute', 'Minutes'],
                'scheduler_interval': 'm'
                },
    'hours': {'variations': ['hour', 'hours', 'Hour', 'Hours'],
              'scheduler_interval': 'h'
              }
}

time_offsets = {'s': 1, 'm': 60, 'h': 3600}


class ReminderSkills(Connection):
    def run(self) -> None:
        """Creates a simple reminder for the given time interval (seconds or minutes or hours)"""

        remind_time = self._get_remind_time('Enter reminder duration: ')
        if remind_time:
            self.send(ResponseType.TEXT_RESPONSE, 'Reminder created', FontStyles.NORMAL)
            self._create_reminder(remind_time)
        else:
            self.send(ResponseType.SKILL_FAIL, "Wrong reminder time", FontStyles.NORMAL)

    def _create_reminder(self, remind_time: int) -> None:
        # Creates new thread
        process = Thread(target=self._remind, args=(self._pipe, remind_time), daemon=True)
        process.start()
        process.run()

    def _get_remind_time(self, text: str) -> int:
        # Gets input from user and returns time in seconds
        remind_time = self.recv_from_speech(text).strip()
        remind_time, unit = self._get_reminder_duration_and_time_interval(remind_time)

        if remind_time:
            return int(remind_time) * time_offsets[unit]

    @staticmethod
    def _remind(pipe, remind_time: int) -> None:
        time.sleep(remind_time)
        pipe.send(Response(ResponseType.TEXT_RESPONSE, 'Time is up'))

    @staticmethod
    def _get_reminder_duration_and_time_interval(text: str) -> Tuple:
        # Extracts the duration and the time interval from the voice transcript.
        # NOTE: If there are multiple time intervals, it will extract the first one.

        for time_interval in time_intervals.values():
            for variation in time_interval['variations']:
                if variation in text:
                    reg_ex = re.search('([0-9]+)', text)
                    duration = reg_ex.group(1)
                    return duration, time_interval['scheduler_interval']
