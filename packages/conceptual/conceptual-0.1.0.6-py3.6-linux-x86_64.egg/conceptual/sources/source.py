import abc
import pathlib
import random
from conceptual import Type

class Source(abc.ABC):
    seed = 42

    def __init__(self, location):
        self.location = location
        if not location.endswith('/'):
            self.location += "/"
        self.attribute_path = self.location + "lexicon/attributes/"
        self.relation_path = self.location + "lexicon/relations/"

        pathlib.Path(self.attribute_path).mkdir(parents=True, exist_ok=True)
        pathlib.Path(self.relation_path).mkdir(parents=True, exist_ok=True)

        self.lexicon = []
        print("Running preprocessing for class '" + type(self).__name__ + "'")
        self.rng = random.Random(Source.seed)
        self.preprocess()

    @abc.abstractmethod
    def preprocess(self):
        raise NotImplementedError

    @abc.abstractmethod
    def sample_word(self, word, t, k, rng):
        raise NotImplementedError

    @staticmethod
    def _sample_from(rng, objects, k):
        if k >= len(objects):
            return objects
        return rng.sample(objects, k)

    def sample(self, word, k=1):
        for (w, t) in self.lexicon:
            if w == word:
                res = self.sample_word(word, t, k, self.rng)
                if k == 1:
                    return res[0]
                else:
                    return res
        print(self.lexicon)
        return None
