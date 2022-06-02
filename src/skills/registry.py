import enum
from .collection import *


class CMD(enum.Enum):
    TAGS = 0
    FUNC = 1
    CLASS = 2


assistant_commands = [
    {
        CMD.TAGS: 'voice',
        CMD.FUNC: 'change_response_to_voice',
        CMD.CLASS: AssistantSkills
    },

    {
        CMD.TAGS: 'text',
        CMD.FUNC: 'change_response_to_text',
        CMD.CLASS: AssistantSkills
    },

    {
        CMD.TAGS: 'wikipedia',
        CMD.FUNC: 'wikipedia',
        CMD.CLASS: BrowserSkills
    },

    {
        CMD.TAGS: 'open',
        CMD.FUNC: 'open_website_in_browser',
        CMD.CLASS: BrowserSkills
    },

    {
        CMD.TAGS: 'search',
        CMD.FUNC: 'search_on_google',
        CMD.CLASS: BrowserSkills
    },

    {
        CMD.TAGS: 'weather',
        CMD.FUNC: 'run',
        CMD.CLASS: WeatherSkills
    },

    {
        CMD.TAGS: 'remind',
        CMD.FUNC: 'run',
        CMD.CLASS: ReminderSkills
    },

    {
        CMD.TAGS: 'synonyms',
        CMD.FUNC: 'show_synonyms',
        CMD.CLASS: BrowserSkills
    },

    {
        CMD.TAGS: 'show calendar',
        CMD.FUNC: 'display_events',
        CMD.CLASS: CalendarSkills
    },

    {
        CMD.TAGS: 'add event',
        CMD.FUNC: 'create_event',
        CMD.CLASS: CalendarSkills
    },

    {
        CMD.TAGS: 'send email',
        CMD.FUNC: 'run',
        CMD.CLASS: EmailSkills
    }
]
