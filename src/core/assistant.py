

class Assistant:
    def __init__(self):
        raise NotImplementedError

    def run(self):
        raise NotImplementedError

    def wake_up(self):
        raise NotImplementedError

    @property
    def parent_connection(self):
        raise NotImplementedError

    @property
    def child_connection(self):
        raise NotImplementedError

    def _response(self):
        raise NotImplementedError
