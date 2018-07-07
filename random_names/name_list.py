import random


class NameList:
    """

    :param name:
    :param tag:
    :param names:
    :param weight:
    :param use_markov:
    :param markov_properties:
    """

    def __init__(self, seed: int, name: str, tag: str, names: list, weight: int,
                 use_markov: bool, markov_properties: dict):
        self._random = random.Random(seed)
        self.name = name
        self.tag = tag
        self.names = names
        self.weight = weight
        self.use_markov = use_markov
        self.markov_properties = markov_properties

    def get_name(self):
        return self._random.choice(self.names)
