from pynput import keyboard
from loguru import logger


class KeyListener:
    def __init__(self, func):
        self._listener = keyboard.Listener(on_press=self._on_press, on_release=self._on_release)
        self._pressed = set()
        self._keys = {keyboard.Key.alt_l, keyboard.KeyCode(char="q")}
        self._func = func

    def start(self):
        """
        Start a listener thread
        """
        self._listener.start()

        return self

    def stop(self):
        """
        Stop a listener thread
        """
        if self._listener.is_alive():
            self._listener.stop()
            self._listener.join()

        return self

    def _on_press(self, key) -> None:
        # adds the pressed key to the set and checks if the sequence matches, then runs the function specified in init
        self._pressed.add(key)
        if self._keys.issubset(self._pressed):
            logger.info("Activation sequence pressed")
            self._func()
            logger.info("Function finished")
            self._pressed.clear()

    def _on_release(self, key) -> None:
        # remove key from the set
        if key in self._pressed:
            self._pressed.remove(key)
