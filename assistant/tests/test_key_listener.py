import unittest
from unittest import mock
from pynput import keyboard

from assistant.core.key_listener import KeyListener


class KeyListenerAsset(unittest.TestCase):
    def setUp(self) -> None:
        self.mock = mock.Mock()
        self.key_listener = KeyListener(self.mock)
        return super().setUp()

    def test_key(self):
        self.key_listener._on_press(keyboard.Key.cmd)
        self.assertIn(keyboard.Key.cmd, self.key_listener._pressed, 'Key not in _pressed set')
        self.key_listener._on_release(keyboard.Key.cmd)
        self.assertNotIn(keyboard.Key.cmd, self.key_listener._pressed, 'Key in _pressed set')

    def test_call_func(self):
        self.key_listener._on_press(keyboard.Key.cmd)
        self.mock.assert_not_called()
        self.key_listener._on_press(keyboard.KeyCode(char="w"))
        self.mock.assert_called()


if __name__ == "__main__":
    unittest.main()
