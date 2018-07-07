from random_names.name_list import NameList
from random_names.name_template import NameTemplate
from random_names.utility import read_name_set_file
import random
import json


class NameSet:
    """"""

    def __init__(self, file_name: str, seed: int):
        self._random = random.Random(8731 + seed)
        self._file_name = file_name
        self._name_set = read_name_set_file(file_name)

        self.id = self._name_set['id']
        self.name = self._name_set['name']

        self.name_lists = dict()
        for nl in self._name_set['name_lists']:
            seed += 1
            self.name_lists[nl['tag']] = NameList(seed, **nl)

        self.templates = dict()
        for temp in self._name_set['templates']:
            self.templates[temp['name']] = NameTemplate(**temp)

    def tags(self):
        result = set()
        for template in self.templates:
            for tag in self.templates[template].tags:
                result.add(tag)
        return result

    def store(self, file_name=None):
        with open(self._file_name if file_name is None else file_name, 'w') as file:
            file.write(json.dumps(self._name_set))





