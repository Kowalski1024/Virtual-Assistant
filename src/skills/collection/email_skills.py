

class EmailSkills:
    @staticmethod
    def send_email():
        raise NotImplementedError

    @staticmethod
    def save_as_draft():
        raise NotImplementedError

    @staticmethod
    def cancel_sending():
        raise NotImplementedError

    @staticmethod
    def _get_email_recipient_address():
        raise NotImplementedError

    @staticmethod
    def _get_subject():
        raise NotImplementedError

    @staticmethod
    def _get_message_content():
        raise NotImplementedError

    @staticmethod
    def _get_attachment_path():
        raise NotImplementedError

