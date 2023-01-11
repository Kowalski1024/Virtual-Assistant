from assistant.recognizer.recognizer import Recognizer


class HandlerBase:
    def handle(self, request):
        raise StopIteration

    @property
    def description(self):
        return 'Unknown'


class VoiceHandlerBase(HandlerBase):
    _recognizer: Recognizer = Recognizer()
