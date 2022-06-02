from multiprocessing import connection

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .. import ResponseType, Connection
from ..skills import CMD, assistant_commands


class SkillMatching(Connection):
    def __init__(self, pipe: connection):
        super().__init__(pipe)
        self._tfid_vectorizer = TfidfVectorizer()
        self._skill_matrix = self._tfid_vectorizer.fit_transform([cmd[CMD.TAGS] for cmd in assistant_commands])

    def run(self):
        skill = None
        while True:
            sentence = self.recv_from_speech()
            match_index, probability = self._find_best_match(sentence)

            if sentence == 'yes' and skill is not None:
                cls = skill[CMD.CLASS](self._pipe)
                getattr(cls, skill[CMD.FUNC])()
                break

            if sentence == 'no':
                continue

            skill = assistant_commands[match_index]
            if probability < 0.5:
                self.send(ResponseType.FAIL_MATCH, f"Sorry no match for \"{sentence}\", please repeat.")
            elif probability < 1:
                self.send(ResponseType.FAIL_MATCH, f"Do you mean {skill[CMD.TAGS]}? Say yes/no or repeat.")
            elif probability == 1:
                cls = skill[CMD.CLASS](self._pipe)
                getattr(cls, skill[CMD.FUNC])()
                break

    def _find_best_match(self, sentence):
        similarities = cosine_similarity(self._skill_matrix, self._tfid_vectorizer.transform([sentence])).flatten()
        best_match_index = similarities.argmax()
        return best_match_index, similarities[best_match_index].round(2)
