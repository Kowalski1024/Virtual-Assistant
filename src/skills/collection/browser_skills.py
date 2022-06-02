import re
import requests
import time
import webbrowser

import wikipedia

from src.enumerations import FontStyles
from src.response import ResponseType, Connection


class BrowserSkills(Connection):
    def search_on_google(self) -> None:
        """Gets keyword from user and opens google.com with search results"""
        key_word = self.recv_from_speech('Enter keyword: ')

        try:
            webbrowser.open_new_tab(f'https://www.google.com/search?q={key_word.replace(" ", "+")}')
            self.send(ResponseType.TEXT_RESPONSE, 'Phrase searched', FontStyles.NORMAL)
        except Exception as e:
            self.send(ResponseType.SKILL_FAIL, 'Cannot find given phrase', FontStyles.NORMAL)

    def open_website_in_browser(self) -> None:
        """
        Gets website name from user.
        Opens a web page in the browser.
        Web page can be in the following formats
            * open www.xxxx.com
            *  open xxxx.com
            *  open xxxx
        Limitations
            - If in the voice_transcript there are more than one commands_dict
              e.g voice_transcript='open youtube and open netflix' the application will find
              and execute only the first one, in our case will open the youtube.
            - Support ONLY the following top domains: '.com', '.org', '.net', '.int', '.edu', '.gov', '.mil', '.pl'
        """
        website = self.recv_from_speech('Enter website: ')
        domain_regex = '([\.a-zA-Z]+)'

        reg_ex = re.search(domain_regex, website)
        try:
            if reg_ex:
                domain = reg_ex.group(1)
                url = self._create_url(domain)

                time.sleep(1)

                webbrowser.open_new_tab(url)
                self.send(ResponseType.TEXT_RESPONSE, 'Browser opened', FontStyles.NORMAL)
        except Exception as e:
            self.send(ResponseType.SKILL_FAIL, 'Cannot open the website', FontStyles.NORMAL)

    def wikipedia(self) -> None:
        """
        Gets keyword from user.
        Searches given keyword on Wikipedia.
        """
        keyword = self.recv_from_speech('Enter keyword: ')

        if keyword not in (ResponseType.SPEECH_ERROR, ResponseType.SPEECH_FAIL):
            try:
                page = wikipedia.page(keyword)
                self.send(ResponseType.TEXT_RESPONSE, page.title, FontStyles.TITLE)
                self.send(ResponseType.TEXT_RESPONSE, page.summary, FontStyles.NORMAL)
            except wikipedia.WikipediaException:
                self.send(ResponseType.SKILL_FAIL, 'Cannot find given keyword', FontStyles.NORMAL)
        else:
            self.send(ResponseType.SKILL_FAIL, 'Invalid keyword', FontStyles.NORMAL)

    def show_synonyms(self):
        word = self.recv_from_speech('Enter word: ')

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

            result = str(sorted(set(result)))  # avoid repeating synonyms
            self.send(ResponseType.TEXT_RESPONSE, result, FontStyles.NORMAL)
        except Exception as e:
            self.send(ResponseType.TEXT_RESPONSE, 'Cannot find any synonyms', FontStyles.NORMAL)

    @staticmethod
    def internet_connectivity_check(url='http://www.google.com/', timeout=2):
        """
            Checks for internet connection availability based on google page.
        """
        try:
            _ = requests.get(url, timeout=timeout)
            return True
        except requests.ConnectionError:
            return False

    @staticmethod
    def _create_url(website: str) -> str:
        # Creates an url. It checks if there is .com suffix and add it if it not exist.

        top_level_domains = ['.com', '.org', '.net', '.int', '.edu', '.gov', '.mil', '.pl']
        url = None
        for top_level_domain in top_level_domains:
            if re.search(top_level_domain, website):
                url = f'https://{website}'

        url = f'https://www.{website}.com' if not url else url
        return url
