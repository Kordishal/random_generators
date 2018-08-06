from procedural_generators.names.name_list import NameList
from procedural_generators.names.name_template import NameTemplate
import random
import json


class NameSet:
    """"""

    def __init__(self, file_name: str, seed: int):
        self._random = random.Random(8731 + seed)
        self._file_name = file_name
        fp = open(file_name)
        name_set = json.load(fp)
        fp.close()

        self.id = name_set['id']
        self.name = name_set['name']

        self.name_lists = dict()
        for nl in name_set['name_lists']:
            seed += 1
            self.name_lists[nl['tag']] = NameList(seed, **nl)

        self.templates = dict()
        for temp in name_set['templates']:
            self.templates[temp['name']] = NameTemplate(**temp)

    @property
    def name_lists_as_list(self):
        return list(self.name_lists.values())

    @property
    def templates_as_list(self):
        return list(self.templates.values())

    def filter_templates(self, tags):
        if tags is None:
            return self.templates_as_list

        templates = self.templates_as_list

        for tag in tags:
            for temp in self.templates_as_list:
                if tag in temp.tags:
                    templates.remove(temp)

        return templates

    def tags(self):
        result = set()
        for template in self.templates:
            for tag in self.templates[template].tags:
                result.add(tag)
        return result

    def store(self, file_name=None):
        with open(self._file_name if file_name is None else file_name, 'w') as file:
            file.write(json.dumps(self._name_set))





