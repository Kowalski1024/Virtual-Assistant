from multiprocessing import connection


class SkillMatching:
    def __init__(self):
        raise NotImplementedError

    def run(self, pipe_connection: connection):
        raise NotImplementedError

    def _find_best_match(self, sentence):
        raise NotImplementedError

