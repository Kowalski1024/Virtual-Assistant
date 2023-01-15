from typing import Callable, Iterable

from loguru import logger
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from assistant.view import GUI
from assistant.recognizer import Recognizer, WhisperRecognizer, GoogleRecognizer
from assistant.assistant_skills import SKILLS
from assistant.observable import ObservableDict


class Controller:
    def __init__(self, view: GUI, model):
        self._view = view
        self._model = model

        self._cancel = False

        self._recognizer = Recognizer()
        self._skill_matching = SkillMatching(skill for skill, func in SKILLS)

        self._available_recognizers = {
            'Whisper': WhisperRecognizer(),
            'GoogleAPI': GoogleRecognizer()
        }

        self.set_recognizer('GoogleAPI')

    def available_recognizers(self) -> list[str]:
        return list(self._available_recognizers.keys())

    def set_recognizer(self, name):
        self._recognizer.set_recognizer(self._available_recognizers[name])

    def cancel(self, state):
        logger.info(f"Cancel button change state to {state}")
        self._cancel = state

    def activate(self):
        self._view.prepare_gui()
        skill = self.find_skill()

        if skill is None:
            self._view.clear_gui()
            return

        name, func = skill
        self._view.set_bottom_text(name)

        data = ObservableDict()
        data.register(self._view.text_frame)

        for description in func(data):
            if self._cancel:
                logger.info("Skill deactivated")
                self._cancel = False
                break

            self._view.set_menu_text(description)

        self._view.clear_gui()

    def find_skill(self):
        while True:
            if self._cancel:
                logger.info("Skill deactivated")
                self._cancel = False
                return None

            try:
                sentence = self._recognizer.transcribe()
            except ValueError as e:
                self._view.set_menu_text(f'{e}')
            else:
                break

        best, similarity = self._skill_matching.find_best_match(sentence)
        skill = SKILLS[best]

        if similarity < 0.7:
            self._view.set_menu_text(f"Sorry no match for \"{sentence}\", please repeat.")
        else:
            self._view.set_menu_text(f"Chosen '{skill[0]}'")

        self._view.show()

        return skill


class SkillMatching:
    def __init__(self, skills: Iterable[str]):
        self._tfid_vectorizer = TfidfVectorizer()
        self._skill_matrix = self._tfid_vectorizer.fit_transform(skills)

    def find_best_match(self, sentence) -> tuple[int, float]:
        # Using cosine similarity returns best match of the input text to the assistant_archive's command set
        similarities = cosine_similarity(self._skill_matrix, self._tfid_vectorizer.transform([sentence])).flatten()
        best_match_index = similarities.argmax()

        return best_match_index, similarities[best_match_index].round(2)