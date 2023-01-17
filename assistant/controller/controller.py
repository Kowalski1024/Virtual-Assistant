from typing import Iterable

from loguru import logger
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from assistant.view import GUI
from assistant.recognizer import Recognizer, WhisperRecognizer, GoogleRecognizer
from assistant.assistant_skills.command import *
from assistant.assistant_skills.skills import Skills
from assistant.observable import ObservableDict
from assistant.model import ReminderModel


class Controller:
    def __init__(self, view: GUI, model: ReminderModel):
        self._view = view
        self._model = model
        self._skills = Skills()

        self._cancel = False

        self._recognizer = Recognizer()

        self._commands: dict[str, Command] = {
            'create event': CreateEvent().configure(self._skills),
            'calendar events': CalendarEvents().configure(self._skills, hide=False),
            'search': Search().configure(self._skills),
            'wikipedia': Wikipedia().configure(self._skills, hide=False),
            'synonyms': Synonyms().configure(self._skills, hide=False),
            'weather': Weather().configure(self._skills, hide=False),
            'create reminder': Reminder().configure(self._skills)
        }

        self._skill_matching = SkillMatching(self._commands)

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
        command = self.find_skill()

        if command is None:
            self._view.clear_gui()
            return

        data = ObservableDict()
        data.register(self._view.text_frame)

        for description in command.execute(data=data):
            if self._cancel:
                logger.info("Skill deactivated")
                self._cancel = False
                break

            self._view.menu_frame.set_info_bar(description)

        if command.hide:
            self._view.clear_gui()

    def find_skill(self) -> Command | None:
        while True:
            if self._cancel:
                logger.info("Skill deactivated")
                self._cancel = False
                return None

            try:
                sentence = self._recognizer.transcribe()
            except ValueError as e:
                self._view.menu_frame.set_info_bar(f'{e}')
            else:
                break

        command_name, similarity = self._skill_matching.find_best_match(sentence)
        command = self._commands[command_name]

        if similarity < 0.7:
            self._view.menu_frame.set_info_bar(f"Sorry no match for \"{sentence}\", please repeat.")
        else:
            self._view.menu_frame.set_info_bar(f"Chosen '{command_name}'")

        self._view.bottom_frame.configure(text=command_name.upper())
        self._view.show()

        return command

    def get_reminders(self):
        return self._model.reminders_now()


class SkillMatching:
    def __init__(self, skills: Iterable[str]):
        self._skills = list(skills)
        self._tfid_vectorizer = TfidfVectorizer()
        self._skill_matrix = self._tfid_vectorizer.fit_transform(self._skills)

    def find_best_match(self, sentence) -> tuple[str, float]:
        # Using cosine similarity returns best match of the input text to the assistant_archive's command set
        similarities = cosine_similarity(self._skill_matrix, self._tfid_vectorizer.transform([sentence])).flatten()
        best_match_index = similarities.argmax()

        return self._skills[best_match_index], similarities[best_match_index].round(2)