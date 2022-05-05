

class Recognizer:
    def __init__(self):
        raise NotImplementedError

    def run(self):
        raise NotImplementedError

    def _get_input(self):
        raise NotImplementedError

    def _speech_to_text(self):
        raise NotImplementedError
