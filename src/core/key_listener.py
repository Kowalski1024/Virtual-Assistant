from pynput import keyboard


class KeyListener:
    def __init__(self, func):
        self._listener = keyboard.Listener(on_press=self._on_press, on_release=self._on_release)
        self._pressed = set()
        self._keys = {keyboard.Key.cmd, keyboard.KeyCode(char="w"), keyboard.Key.ctrl_l}
        self._func = func

    def start(self):
        self._listener.start()

    def stop(self):
        if self._listener.is_alive():
            self._listener.stop()
            self._listener.join()

    def _on_press(self, key):
        self._pressed.add(key)
        if self._keys.issubset(self._pressed):
            self._func()

    def _on_release(self, key):
        if key in self._pressed:
            self._pressed.remove(key)
