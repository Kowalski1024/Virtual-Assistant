from email.utils import parseaddr
from typing import Tuple

import win32com.client

from assistant.enumerations import FontStyles
from assistant.response import Connection, ResponseType

options = {
    'send': 1,
    'save': 2,
    'cancel': 3
}


class EmailSkills(Connection):
    def run(self) -> None:
        """Gives input from user to prepare mail, sends it or saves as draft or cancels it.
        Limitations:
            * Mail cancelling can only take place while writing mail content
        """

        outlook = win32com.client.Dispatch('Outlook.Application')
        mail = outlook.CreateItem(0)
        mail.subject, mail.To, mail.Body, option = self._prepare_email()

        if option == 1:
            self._send_email(mail)
        elif option == 2:
            self._save_as_draft(mail)
        else:
            self._cancel_sending()

    def _send_email(self, mail) -> None:
        # Sends mail given as parameter and prints suitable message
        mail.send()
        self.send(ResponseType.TEXT_RESPONSE, 'Email sent', FontStyles.NORMAL)

    def _save_as_draft(self, mail) -> None:
        # Saves mail as draft and prints suitable message
        mail.save()
        self.send(ResponseType.TEXT_RESPONSE, 'Email saved as draft', FontStyles.NORMAL)

    def _cancel_sending(self) -> None:
        self.send(ResponseType.TEXT_RESPONSE, 'Email cancelled', FontStyles.NORMAL)

    def _prepare_email(self) -> Tuple:
        # Gets fom user recipient address, subject, content of an email and what to do with it (save, save, cancel
        to = self._get_email_recipient_address('Enter email recipient address: ')
        subject = self._get_subject('Say subject')
        content, option = self._get_message_content_and_command('Say content: ')

        return subject, to, content, option

    def _get_email_recipient_address(self, text: str) -> str:
        # Gets email recipient address from user as long as it's not valid
        while True:
            self.send(ResponseType.WAITING_FOR_TEXT_INPUT, '', FontStyles.NORMAL)
            email_address = self.recv()
            if parseaddr(email_address)[1]:
                break
            self.send(ResponseType.TEXT_RESPONSE, 'Invalid email format', FontStyles.NORMAL)
        return email_address

    def _get_subject(self, text: str) -> str:
        # Gets email subject from user
        subject = self.recv_from_speech(text)
        subject = subject.strip()

        return subject

    def _get_message_content_and_command(self, text: str) -> Tuple:
        # Gets email content from user
        content = ''
        phrase = self.recv_from_speech(text)

        while phrase.lower() not in ('send', 'save', 'cancel'):
            content += f' {phrase}'
            phrase = self.recv_from_speech()

        return content, options[phrase]
