from random_names.name_list import NameList
from random_names.name_template import NameTemplate
from random_names.utility import read_name_set_file, check_name_set
import random


class NameSet:
    """"""

    def __init__(self, file_name: str, seed: int):
        self.random = random.Random(8731 + seed)
        name_set = read_name_set_file(file_name)

        check_name_set(name_set)

        self.id = name_set['id']
        self.name = name_set['name']

        self.name_lists = dict()
        for nl in name_set['name_lists']:
            self.name_lists[nl['tag']] = NameList(**nl)

        self.templates = dict()
        for temp in name_set['templates']:
            self.templates[temp['name']] = NameTemplate(**temp)

    def get_name(self) -> str:
        name_list = random.sample(self.name_lists, 1)
        return random.choice(name_list.names)

    def get_name_from_name_list_tag(self, name_list_tag: str) -> str:
        for name_list in self.core.name_lists:
            if name_list_tag == name_list.tag:
                # TODO: insert code to use markov chains when markov properties are present.
                length = len(name_list['names'])
                return name_list['names'][random.randrange(length)]

    def get_name_list_tags(self):
        return self.name_lists.keys()

    def add_names_to_namelist(self, names: list, name_list_tag: str):
        if name_list_tag in self.name_lists:
            self.name_lists[name_list_tag]['names'].append(names)
        else:
            raise Exception()

    def __repr__(self):
        return json.dumps(self.core.__dict__, indent='    ', ensure_ascii=False)

