import unittest
from assistant.skills.collection.email_skills import EmailSkills
from multiprocessing import Pipe, Process
from assistant.response import ResponseType, Response


class EmailTests(unittest.TestCase):
    def setUp(self) -> None:
        self.parent, self.child = Pipe()
        self.email_skills = EmailSkills(self.child)
        return super().setUp()

    def tearDown(self) -> None:
        self.parent.close()
        self.child.close()

    def test_mail_recipients(self):
        process = Process(target=self.email_skills.run, daemon=True)
        process.start()
        data: Response = self.parent.recv()
        # two invalid and then one valid address
        self.parent.send(Response(ResponseType.TEXT_RESPONSE, 'arkadiusz.bialy@@onet.pl'))
        data: Response = self.parent.recv()
        self.assertEqual(data.message, 'Invalid email format')

        data: Response = self.parent.recv()
        self.parent.send(Response(ResponseType.TEXT_RESPONSE, 'arkadiuszbialy@onet@pl'))
        data: Response = self.parent.recv()
        self.assertEqual(data.message, 'Invalid email format')

        data: Response = self.parent.recv()
        self.parent.send(Response(ResponseType.TEXT_RESPONSE, 'arkadiusz.bialy@onet.pl'))
        data: Response = self.parent.recv()
        self.assertNotEqual(data.message, 'Invalid email format')
        process.terminate()

    


if __name__ == "__main__":
    unittest.main()
