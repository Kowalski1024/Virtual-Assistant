from assistant.handlers.handler_base import HandlerBase


class ChainDescriptionIterator:
    def __init__(self, handlers: list[HandlerBase], request):
        self._handlers = handlers
        self._request = request
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        handler = None

        try:
            handler = self._handlers[self._index]
            self._request = handler.handle(self._request)
        except ValueError as e:
            if handler:
                return f"{e} {handler.description}"
            else:
                return e
        else:
            self._index += 1

        return handler.description
