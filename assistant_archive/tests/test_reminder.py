import unittest
import time

from assistant_archive.skills.collection.reminder_skills import ReminderSkills
from multiprocessing import Pipe, Process
from assistant_archive.response import ResponseType, Response


def test_reminder_valid_data(reminder, time_unit):
    process = Process(target=reminder.reminder.run, daemon=True)
    process.start()
    data: Response = reminder.parent.recv()
    reminder.assertIs(ResponseType.WAITING_FOR_SPEECH_INPUT, data.type)
    reminder.parent.send(Response(ResponseType.TEXT_RESPONSE, time_unit))
    data: Response = reminder.parent.recv()
    reminder.assertEqual(data.message, 'Reminder created')
    process.terminate()


def test_reminder_invalid_data(reminder, time_unit):
    process = Process(target=reminder.reminder.run, daemon=True)
    process.start()
    data: Response = reminder.parent.recv()
    reminder.assertIs(ResponseType.WAITING_FOR_SPEECH_INPUT, data.type)
    reminder.parent.send(Response(ResponseType.TEXT_RESPONSE, time_unit))
    data: Response = reminder.parent.recv()
    reminder.assertEqual(data.message, 'Wrong reminder time')
    process.terminate()


class ReminderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.parent, self.child = Pipe()
        self.reminder = ReminderSkills(self.child)
        return super().setUp()

    def tearDown(self) -> None:
        self.parent.close()
        self.child.close()

    def test_reminder_minutes(self):
        test_reminder_valid_data(self, '20 minutes')

    def test_reminder_minutes_invalid(self):
        test_reminder_invalid_data(self, '0 minutes')

    def test_reminder_hours(self):
        test_reminder_valid_data(self, '25 hours')

    def test_reminder_hours_invalid(self):
        test_reminder_invalid_data(self, '0 Hours')

    def test_reminder_seconds(self):
        test_reminder_valid_data(self, '10 seconds')

    def test_reminder_seconds_invalid(self):
        test_reminder_invalid_data(self, '-0 seconds')

    def test_reminder_finish(self):
        process = Process(target=self.reminder.run, daemon=True)
        process.start()
        data: Response = self.parent.recv()
        self.assertIs(ResponseType.WAITING_FOR_SPEECH_INPUT, data.type)
        self.parent.send(Response(ResponseType.TEXT_RESPONSE, '2 seconds'))
        data: Response = self.parent.recv()
        data: Response = self.parent.recv()
        self.assertEqual(data.message, 'Time is up')
        process.terminate()


if __name__ == "__main__":
    unittest.main()
