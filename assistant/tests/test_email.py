import unittest
from assistant.skills.collection.email_skills import EmailSkills
from multiprocessing import Pipe, Process
from assistant.response import ResponseType, Response


class EmailTests(unittest.TestCase):
    def setUp(self) -> None:
        self.parent, self.child = Pipe()
        self.email_skills = EmailSkills(self.child)
        self.process = Process(target=self.email_skills.run, daemon=True)
        self.process.start()
        return super().setUp()

    def tearDown(self) -> None:
        self.process.terminate()
        self.parent.close()
        self.child.close()

    def test_mail_recipients(self):
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

    def test_cancel(self):
        data: Response = self.parent.recv()

        self.parent.send(Response(ResponseType.TEXT_RESPONSE, 'r@r.com.pl'))
        data: Response = self.parent.recv()

        self.parent.send(Response(ResponseType.TEXT_RESPONSE, 'xd'))  # subject
        data: Response = self.parent.recv()

        self.parent.send(Response(ResponseType.TEXT_RESPONSE, 'cancel'))  # option
        data: Response = self.parent.recv()

        self.assertEqual(data.message, 'Email cancelled')

    # If someone want test it...

    # def test_save_as_draft(self):
    #     data: Response = self.parent.recv()
    #
    #     self.parent.send(Response(ResponseType.TEXT_RESPONSE, 'arkadiusz.bialy@onet.pl'))
    #     data: Response = self.parent.recv()
    #
    #     self.parent.send(Response(ResponseType.TEXT_RESPONSE, 'empty'))  # subject
    #     data: Response = self.parent.recv()
    #
    #     # self.parent.send(Response(ResponseType.TEXT_RESPONSE, 'random'))  # email body
    #     # data: Response = self.parent.recv()
    #
    #     self.parent.send(Response(ResponseType.TEXT_RESPONSE, 'save'))  # option
    #     data: Response = self.parent.recv()
    #
    #     self.assertEqual(data.message, 'Email saved as draft')

    # def test_send(self):
    #     data: Response = self.parent.recv()
    #
    #     self.parent.send(Response(ResponseType.TEXT_RESPONSE, 'smth@smth.com'))
    #     data: Response = self.parent.recv()
    #
    #     self.parent.send(Response(ResponseType.TEXT_RESPONSE, 'a'))  # subject
    #     data: Response = self.parent.recv()
    #
    #     self.parent.send(Response(ResponseType.TEXT_RESPONSE, 'send'))  # option
    #     data: Response = self.parent.recv()
    #
    #     self.assertEqual(data.message, 'Email sent')


if __name__ == "__main__":
    unittest.main()
