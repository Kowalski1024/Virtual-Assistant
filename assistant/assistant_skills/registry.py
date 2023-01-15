from typing import Callable


from assistant.assistant_skills.skills import Skills


_skills = Skills()


SKILLS: list[tuple[str, Callable]] = [
    ('create event', _skills.create_event_in_calendar)
]
