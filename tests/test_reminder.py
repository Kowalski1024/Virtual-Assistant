import unittest

from src.skills.collection.reminder_skills import ReminderSkills
from multiprocessing import Pipe, Process
from src.response import ResponseType, Response


class ReminderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.parent, self.child = Pipe()
        self.reminder = ReminderSkills(self.child)
        return super().setUp()

    def test_reminder(self):
        process = Process(target=self.reminder.create_reminder, daemon=True)
        process.start()
        data: Response = self.parent.recv()
        self.assertIs(ResponseType.WAITING_FOR_SPEECH_INPUT, data.type)
        self.parent.send(Response(ResponseType.TEXT_RESPONSE, '10 seconds'))
        data: Response = self.parent.recv()
        self.assertEqual(data.message, 'Cannot create reminder')


if __name__ == "__main__":
    unittest.main()

