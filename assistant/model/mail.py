from email.utils import parseaddr

import win32com.client


class MailModel:
    def __init__(self):
        self._email = None
        self._subject = None
        self._message = None

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value: str):
        if parseaddr(value)[1]:
            self._email = value
        else:
            raise ValueError(f'Invalid email address: {value}')

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value: str):
        self._message = value

    @property
    def subject(self):
        return self._message

    @subject.setter
    def subject(self, value: str):
        self._message = value

    def add_message(self, value: str):
        self._message = f'{self._message} {value}'

    # def send(self):
    #     self.get_mail(self.email, self.subject, self.message).send()
    #
    # def save(self):
    #     self.get_mail(self.email, self.subject, self.message).save()
    #
    # @classmethod
    # def get_mail(cls, to: str, subject: str, body: str):
    #     mail = cls.CLIENT.CreateItem(0)
    #     mail.To = to
    #     mail.subject = subject
    #     mail.Body = body
    #
    #     return mail

