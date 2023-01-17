from typing import Callable

from assistant.assistant_skills.skills import Skills

_skills = Skills()

SKILLS: list[dict] = [
    {
        'command': 'create event',
        'func': _skills.create_event_in_calendar,
    },
    {
        'command': 'search',
        'func': _skills.google_search,
    },
    {
        'command': 'wikipedia',
        'func': _skills.wikipedia,
        'hide': False
    },
    {
        'command': 'synonyms',
        'func': _skills.synonyms,
        'hide': False
    },
    {
        'command': 'calendar events',
        'func': _skills.display_event_in_calendar,
        'hide': False
    },
    {
        'command': 'weather',
        'func': _skills.weather,
        'hide': False
    },
{
        'command': 'create reminder',
        'func': _skills.create_reminder,
    }
]
