

class NameList:
    """

    :param name:
    :param tag:
    :param names:
    :param weight:
    :param use_markov:
    :param markov_order:
    :param markov_min_length:
    :param markov_max_length:
    """

    def __init__(self, name: str, tag: str, names: list, weight: int,
                 use_markov=False, markov_order=0, markov_min_length=0, markov_max_length=0):
        self.name = name
        self.tag = tag
        self.names = names
        self.weight = weight
        self.use_markov = use_markov
        self.markov_order = markov_order
        self.markov_min_length = markov_min_length
        self.markov_max_length = markov_max_length
