import webbrowser

import wikipedia

import requests

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

    def show_synonyms():
        word = self.recv_from_speech()

        try:
            url = f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}'
            response = requests.get(url)
            data = response.json()

            result = []
            no_of_words = len(data)
            
            # We iterate through the whole API response, because synonyms can be in different places
            for q in range(no_of_words):
                no_of_meanings = len(data[q]['meanings'])
                for i in range(no_of_meanings):
                    for synonym in data[q]['meanings'][i]['synonyms']:
                        result.append(synonym) 

                    no_of_definitions = len(data[q]['meanings'][i]['definitions'])
                    for j in range(no_of_definitions):
                        for synonym in data[q]['meanings'][i]['definitions'][j]['synonyms']:
                            result.append(synonym)

            result = str(sorted(set(result))) # avoid repeating synonyms
            self.send(ResponseType.TEXT_RESPONSE, result, FontStyles.NORMAL)
        except Exception as e:
            self.send(ResponseType.TEXT_RESPONSE, 'Cannot find any synonyms', FontStyles.NORMAL)

    @staticmethod
    def internet_connectivity_check():
        raise NotImplementedError

    @staticmethod
    def _create_url():
        raise NotImplementedError
