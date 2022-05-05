

class KeyListener:
    def __init__(self):
        raise NotImplementedError

    def start(self):
        raise NotImplementedError

    def stop(self):
        raise NotImplementedError

    def _on_press(self):
        raise NotImplementedError

    def _on_release(self):
        raise NotImplementedError
