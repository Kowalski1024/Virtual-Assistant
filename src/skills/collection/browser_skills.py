import wikipedia

from src.enumerations import FontStyles
from src.response import ResponseType, Connection


class BrowserSkills(Connection):
    @staticmethod
    def search_on_google():
        raise NotImplementedError

    @staticmethod
    def open_website_in_browser():
        raise NotImplementedError

    def wikipedia(self):
        keyword = self.recv_from_speech()

        if keyword not in (ResponseType.SPEECH_ERROR, ResponseType.SPEECH_FAIL):
            try:
                page = wikipedia.page(keyword)
                self.send(ResponseType.TEXT_RESPONSE, page.title, FontStyles.TITLE)
                self.send(ResponseType.TEXT_RESPONSE, page.summary, FontStyles.NORMAL)
            except wikipedia.WikipediaException:
                self.send(ResponseType.SKILL_FAIL, 'Cannot find given keyword', FontStyles.NORMAL)
        else:
            self.send(ResponseType.SKILL_FAIL, 'Invalid keyword', FontStyles.NORMAL)


    @staticmethod
    def show_synonyms():
        raise NotImplementedError

    @staticmethod
    def internet_connectivity_check():
        raise NotImplementedError

    @staticmethod
    def _create_url():
        raise NotImplementedError
