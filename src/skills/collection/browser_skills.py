import re
import time
import webbrowser

import wikipedia

from src.enumerations import FontStyles
from src.response import ResponseType, Connection


class BrowserSkills(Connection):
    def search_on_google(self):
        key_word = self.recv_from_speech('Enter keyword: ')

        try:
            webbrowser.open_new_tab(f'https://www.google.com/search?q={key_word.replace(" ", "+")}')
            self.send(ResponseType.TEXT_RESPONSE, 'Phrase searched', FontStyles.NORMAL)
        except Exception as e:
            self.send(ResponseType.SKILL_FAIL, 'Cannot find given phrase', FontStyles.NORMAL)

    def open_website_in_browser(self):
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
    def _create_url(domain):
        top_level_domains = ['.com', '.org', '.net', '.int', '.edu', '.gov', '.mil', '.pl']
        url = None
        for top_level_domain in top_level_domains:
            if re.search(top_level_domain, domain):
                url = f'https://{domain}'

        url = f'https://www.{domain}.com' if not url else url
        return url
