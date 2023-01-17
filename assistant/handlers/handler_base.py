from assistant.recognizer.recognizer import Recognizer


class HandlerBase:
    def __init__(self, key=None, description='Unknown'):
        self._key = key
        self._desc = description

    def handle(self, request):
        raise StopIteration

    @property
    def description(self):
        return self._desc


class VoiceHandlerBase(HandlerBase):
    _recognizer: Recognizer = Recognizer()
