import random
import textwrap


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

        if use_markov:
            self.markov_properties = markov_properties
            self.alphabet, self.starting_particles = self._markov_generation()

    def _markov_generation(self):
        order = self.markov_properties['order']
        alphabet = dict()
        starting_particles = list()

        for name in self.names:
            wrapped = textwrap.wrap(name, order)
            starting_particles.append(wrapped[0])
            if len(wrapped) == 1:
                if wrapped[0] in alphabet:
                    alphabet[wrapped[0]].append(wrapped[0])
                else:
                    alphabet[wrapped[0]] = [wrapped[0]]
            for i in range(len(wrapped) - 1):
                if wrapped[i] in alphabet:
                    alphabet[wrapped[i]].append(wrapped[i + 1])
                else:
                    alphabet[wrapped[i]] = [wrapped[i + 1]]

        return alphabet, starting_particles

    def _get_name_from_markov(self):
        result = self._random.choice(self.starting_particles)
        next_part = self._random.choice(self.alphabet[result])
        while len(result) <= self.markov_properties['length'][1]:
            result += next_part
            if next_part in self.alphabet:
                next_part = self._random.choice(self.alphabet[next_part])
            else:
                break
        return result

    def get_name(self):
        if self.use_markov:
            return self._get_name_from_markov()
        else:
            return self._random.choice(self.names)
