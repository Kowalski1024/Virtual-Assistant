from typing import Optional
from multiprocessing import connection

from dataclasses import dataclass
from enumerations import ResponseType, FontStyles


@dataclass
class Response:
    type: ResponseType
    message: Optional[str] = None
    font: Optional[FontStyles] = None


class Connection:
    def __init__(self, pipe: connection):
        self._pipe = pipe

    def send(self, response_type: ResponseType, message: Optional[str] = None, font: Optional[FontStyles] = None):
        self._pipe.send(Response(response_type, message, font))

    def recv(self):
        data: Response = self._pipe.recv()
        return data.message

    def recv_from_speech(self):
        self._pipe.send(Response(ResponseType.WAITING_FOR_SPEECH_INPUT))
        data: Response = self._pipe.recv()
        return data.message