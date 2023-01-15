from typing import Callable


from assistant.handlers.handler_base import HandlerBase


class HandlerDescriptionIterator:
    def __init__(self, handlers: list[HandlerBase]):
        self._handlers = handlers
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self) -> tuple[str, Callable]:
        if self._index == len(self._handlers):
            raise StopIteration

        handler = self._handlers[self._index]
        self._index += 1

        return handler.description, handler.handle
