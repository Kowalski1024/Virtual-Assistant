from multiprocessing import connection
from dataclasses import dataclass

from .enumerations import ResponseType, FontStyles


@dataclass
class Response:
    type: ResponseType
    message: str = None
    font: FontStyles = None


class Connection:
    def __init__(self, pipe: connection):
        self._pipe = pipe

    def send(self, response_type: ResponseType, message: str = None, font: FontStyles = None):
        """
        Sending Response by pipe connection
        """
        self._pipe.send(Response(response_type, message, font))

    def recv(self) -> str:
        """
        Receiving message from pipe connection
        :return: text message
        """
        data: Response = self._pipe.recv()
        return data.message

    def recv_from_speech(self, text: str = None) -> str:
        """
        Receiving speech input from user
        :param text: additional information for user
        :return: user speech input as text
        """
        while True:
            self._pipe.send(Response(ResponseType.WAITING_FOR_SPEECH_INPUT, text, FontStyles.TITLE))
            data: Response = self._pipe.recv()
            if data.type == ResponseType.TEXT_RESPONSE:
                break
            else:
                self.send(data.type, data.message)
        return data.message
