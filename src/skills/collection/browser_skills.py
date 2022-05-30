import webbrowser

import wikipedia

from src.enumerations import FontStyles
from src.response import ResponseType, Connection


class BrowserSkills(Connection):
    def search_on_google(self):
        key_word = self.recv_from_speech()

        try:
            webbrowser.open_new_tab(f'https://www.google.com/search?q={key_word.replace(" ", "+")}')
            self.send(ResponseType.TEXT_RESPONSE, 'Phrase searched', FontStyles.NORMAL)
        except Exception as e:
            self.send(ResponseType.SKILL_FAIL, 'Cannot find given phrase', FontStyles.NORMAL)

    @staticmethod
    def open_website_in_browser(self):
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
