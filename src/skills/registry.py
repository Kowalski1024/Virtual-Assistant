import enum
from .collection import *


class Command(enum.Enum):
    TAGS = 0
    FUNC = 1
    CLASS = 2


COMMANDS = [
    {
        Command.TAGS: 'wikipedia',
        Command.FUNC: 'wikipedia',
        Command.CLASS: BrowserSkills
    },

    {
        Command.TAGS: 'show calendar',
        Command.FUNC: None,
    },

    {
        Command.TAGS: 'open',
        Command.FUNC: 'open_website_in_browser',
        Command.CLASS: BrowserSkills
    },

    {
        Command.TAGS: 'search',
        Command.FUNC: 'search_in_google',
        Command.CLASS: BrowserSkills
    },

    {
        Command.TAGS: 'weather',
        Command.FUNC: 'run',
        Command.CLASS: WeatherSkills
    },

    {
        Command.TAGS: 'remind',
        Command.FUNC: 'create_reminder',
        Command.CLASS: ReminderSkills
    }
]