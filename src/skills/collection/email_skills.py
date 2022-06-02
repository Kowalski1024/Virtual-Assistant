from email.utils import parseaddr

import win32com.client

from src.enumerations import FontStyles
from src.response import ResponseType, Connection

options = {
    'send': 1,
    'save': 2,
    'cancel': 3
}


class EmailSkills(Connection):
    def run(self):
        outlook = win32com.client.Dispatch('Outlook.Application')
        mail = outlook.CreateItem(0)
        mail.subject, mail.To, mail.Body, option = self._prepare_email()

        if option == 1:
            self._send_email(mail)
        elif option == 2:
            self._save_as_draft(mail)
        else:
            self._cancel_sending()

    def _send_email(self, mail):
        mail.send()
        self.send(ResponseType.TEXT_RESPONSE, 'Email sent', FontStyles.NORMAL)

    def _save_as_draft(self, mail):
        mail.save()
        self.send(ResponseType.TEXT_RESPONSE, 'Email saved as draft', FontStyles.NORMAL)

    def _cancel_sending(self):
        self.send(ResponseType.TEXT_RESPONSE, 'Email cancelled', FontStyles.NORMAL)

    def _prepare_email(self):
        to = self._get_email_recipient_address('Enter email recipient address: ')
        subject = self._get_subject('Enter subject: ')
        content, option = self._get_message_content_and_command('Enter content: ')

        return subject, to, content, option

    def _get_email_recipient_address(self, text=''):
        while True:
            self.send(ResponseType.WAITING_FOR_TEXT_INPUT, '', FontStyles.NORMAL)
            email_address = self.recv()
            if parseaddr(email_address)[1]:
                break
            self.send(ResponseType.TEXT_RESPONSE, 'Invalid email format', FontStyles.NORMAL)
        return email_address

    def _get_subject(self, text):
        subject = self.recv_from_speech(text)
        subject = subject.strip()

        return subject

    def _get_message_content_and_command(self, text):
        content = ''
        phrase = self.recv_from_speech(text)

        while phrase.lower() not in ('send', 'cancel', 'save', 'Send', 'Cancel', 'Save'):
            content += f' {phrase}'
            phrase = self.recv_from_speech()

        return content, options[phrase]
