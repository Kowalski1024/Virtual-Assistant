from src.enumerations import FontStyles
from src.response import ResponseType, Connection


class AssistantSkills(Connection):
    def change_response_to_voice(self):
        self.send(ResponseType.CHANGE_RESPONSE, 'voice')

    def change_response_to_text(self):
        self.send(ResponseType.CHANGE_RESPONSE, 'text')
