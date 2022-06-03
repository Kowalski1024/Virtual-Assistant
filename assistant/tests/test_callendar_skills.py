import unittest
from assistant.skills.collection.calendar_skills import CalendarSkills
from multiprocessing import Pipe, Process
from assistant.response import ResponseType, Response

expected_result = 'Subject: empty\nPlace: Cracow\nStart time: 2022-08-29 20:00:00+00:00\nEnd time: 2022-08-29 ' \
                  '20:20:00+00:00\nText: \nSubject: empty\nPlace: Cracow\nStart time: 2022-08-30 21:00:00+00:00\nEnd ' \
                  'time: 2022-08-30 21:25:00+00:00\nText: '


class CalendarTests(unittest.TestCase):
    def setUp(self) -> None:
        self.parent, self.child = Pipe()
        self.calendar_skills = CalendarSkills(self.child)
        return super().setUp()

    def tearDown(self) -> None:
        self.parent.close()
        self.child.close()

    def test_creating_event(self):
        process = Process(target=self.calendar_skills.create_event, daemon=True)
        process.start()
        data: Response = self.parent.recv()
        self.assertIs(ResponseType.WAITING_FOR_SPEECH_INPUT, data.type)
        self.parent.send(Response(ResponseType.TEXT_RESPONSE, '2022-05-06'))
        data: Response = self.parent.recv()
        self.assertNotEqual(data.message, 'Wrong date')
        self.parent.send(Response(ResponseType.TEXT_RESPONSE, '12:34'))
        data: Response = self.parent.recv()
        self.assertNotEqual(data.message, 'Wrong hour')
        self.parent.send(Response(ResponseType.TEXT_RESPONSE, 'Meeting'))
        data: Response = self.parent.recv()
        self.parent.send(Response(ResponseType.TEXT_RESPONSE, '25'))
        data: Response = self.parent.recv()
        self.assertNotEqual(data.message, 'Duration time is not a number')
        self.parent.send(Response(ResponseType.TEXT_RESPONSE, 'Warsaw'))
        data: Response = self.parent.recv()
        result = data.message.split(' ')
        self.assertTrue(
            result[0] == '2022-05-06' and result[1] == '12:34:00+00:00' and result[2] == 'Meeting' and result[
                3] == '25' and
            result[4] == 'Warsaw',
            'Event was not created')
        process.terminate()

    def test_wrong_date(self):
        process = Process(target=self.calendar_skills.create_event, daemon=True)
        process.start()
        data: Response = self.parent.recv()
        self.assertIs(ResponseType.WAITING_FOR_SPEECH_INPUT, data.type)
        self.parent.send(Response(ResponseType.TEXT_RESPONSE, '0-0-0'))
        data: Response = self.parent.recv()
        self.assertEqual(data.message, 'Wrong date')
        process.terminate()

    def test_wrong_hour(self):
        process = Process(target=self.calendar_skills.create_event, daemon=True)
        process.start()
        data: Response = self.parent.recv()
        self.assertIs(ResponseType.WAITING_FOR_SPEECH_INPUT, data.type)
        self.parent.send(Response(ResponseType.TEXT_RESPONSE, '2022.06.05'))
        data: Response = self.parent.recv()
        self.assertNotEqual(data.message, 'Wrong date')
        self.parent.send(Response(ResponseType.TEXT_RESPONSE, '24:12'))
        data: Response = self.parent.recv()
        self.assertEqual(data.message, 'Wrong hour')
        process.terminate()

    def test_wrong_duration(self):
        process = Process(target=self.calendar_skills.create_event, daemon=True)
        process.start()
        data: Response = self.parent.recv()
        self.assertIs(ResponseType.WAITING_FOR_SPEECH_INPUT, data.type)
        self.parent.send(Response(ResponseType.TEXT_RESPONSE, '2022.06.05'))
        data: Response = self.parent.recv()
        self.assertNotEqual(data.message, 'Wrong date')
        self.parent.send(Response(ResponseType.TEXT_RESPONSE, '23:12'))
        data: Response = self.parent.recv()
        self.assertNotEqual(data.message, 'Wrong hour')
        self.parent.send(Response(ResponseType.TEXT_RESPONSE, 'random'))
        data: Response = self.parent.recv()
        self.parent.send(Response(ResponseType.TEXT_RESPONSE, '-8'))
        data: Response = self.parent.recv()
        self.assertEqual(data.message, 'Duration time is not a number')
        process.terminate()

    def test_displaying_events(self):
        process = Process(target=self.calendar_skills.display_events, daemon=True)
        process.start()
        data: Response = self.parent.recv()
        self.assertIs(ResponseType.WAITING_FOR_SPEECH_INPUT, data.type)
        # test for no events
        self.parent.send(Response(ResponseType.TEXT_RESPONSE, '2034-10-10'))
        data: Response = self.parent.recv()
        self.parent.send(Response(ResponseType.TEXT_RESPONSE, '2034-10-10'))
        data: Response = self.parent.recv()
        self.assertEqual(data.message, 'No events found')
        # test for some events in calendar
        process.terminate()
        self.tearDown()
        self.setUp()
        process1 = Process(target=self.calendar_skills.create_event, daemon=True)
        process1.start()
        # 1st event
        data: Response = self.parent.recv()
        self.assertIs(ResponseType.WAITING_FOR_SPEECH_INPUT, data.type)
        self.parent.send(Response(ResponseType.TEXT_RESPONSE, '2022-08-29'))
        data: Response = self.parent.recv()
        self.parent.send(Response(ResponseType.TEXT_RESPONSE, '20:00'))
        data: Response = self.parent.recv()
        self.parent.send(Response(ResponseType.TEXT_RESPONSE, 'empty'))
        data: Response = self.parent.recv()
        self.parent.send(Response(ResponseType.TEXT_RESPONSE, '20'))
        data: Response = self.parent.recv()
        self.parent.send(Response(ResponseType.TEXT_RESPONSE, 'Cracow'))
        data: Response = self.parent.recv()

        process1.terminate()
        self.tearDown()
        self.setUp()

        process1 = Process(target=self.calendar_skills.create_event, daemon=True)
        process1.start()
        data: Response = self.parent.recv()
        self.assertIs(ResponseType.WAITING_FOR_SPEECH_INPUT, data.type)

        # 2nd event
        self.parent.send(Response(ResponseType.TEXT_RESPONSE, '2022-08-30'))
        data: Response = self.parent.recv()
        self.parent.send(Response(ResponseType.TEXT_RESPONSE, '21:00'))
        data: Response = self.parent.recv()
        self.parent.send(Response(ResponseType.TEXT_RESPONSE, 'empty'))
        data: Response = self.parent.recv()
        self.parent.send(Response(ResponseType.TEXT_RESPONSE, '25'))
        data: Response = self.parent.recv()
        self.parent.send(Response(ResponseType.TEXT_RESPONSE, 'Cracow'))
        data: Response = self.parent.recv()

        process1.terminate()
        self.tearDown()
        self.setUp()

        # test if events are present
        process2 = Process(target=self.calendar_skills.display_events, daemon=True)
        process2.start()
        data: Response = self.parent.recv()
        self.assertIs(ResponseType.WAITING_FOR_SPEECH_INPUT, data.type)
        self.parent.send(Response(ResponseType.TEXT_RESPONSE, '2022-08-29'))
        data: Response = self.parent.recv()
        self.parent.send(Response(ResponseType.TEXT_RESPONSE, '2022-08-30'))
        data: Response = self.parent.recv()
        self.assertNotEqual(data.message, expected_result)

        process2.terminate()


if __name__ == "__main__":
    unittest.main()
