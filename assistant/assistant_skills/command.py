from assistant.assistant_skills.skills import Skills


__all__ = [
    'Command',
    'CreateEvent',
    'CalendarEvents',
    'Wikipedia',
    'Search',
    'Synonyms',
    'Weather',
    'Reminder'
]


class Command:
    def __init__(self):
        self.params: dict | None = None
        self.receiver: Skills | None = None

    @property
    def hide(self) -> str:
        return self.params.get('hide', True)

    def execute(self, **kwargs):
        raise NotImplementedError

    def configure(self, receiver, **kwargs) -> 'Command':
        self.receiver = receiver
        self.params = kwargs
        return self


class CreateEvent(Command):
    def execute(self, **kwargs):
        self.receiver.create_event_in_calendar(**kwargs)


class CalendarEvents(Command):
    def execute(self, **kwargs):
        self.receiver.google_search(**kwargs)


class Wikipedia(Command):
    def execute(self, **kwargs):
        self.receiver.wikipedia(**kwargs)


class Search(Command):
    def execute(self, **kwargs):
        self.receiver.google_search(**kwargs)


class Synonyms(Command):
    def execute(self, **kwargs):
        self.receiver.synonyms(**kwargs)


class Weather(Command):
    def execute(self, **kwargs):
        self.receiver.weather(**kwargs)


class Reminder(Command):
    def execute(self, **kwargs):
        self.receiver.create_reminder(**kwargs)
