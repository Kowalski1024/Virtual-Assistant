import enum


class ResponseType(enum.Enum):
    WAITING_FOR_TEXT_INPUT = 100
    WAITING_FOR_SPEECH_INPUT = 101
    TEXT_RESPONSE = 200
    FAIL_MATCH = 300
    SKILL_FAIL = 301
    SPEECH_FAIL = 302
    SPEECH_ERROR = 303


class FontStyles(enum.Enum):
    pass


class Colors(enum.Enum):
    pass
