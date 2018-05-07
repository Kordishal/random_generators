from random_names.utility import read_name_set_file

import random




class NameSet:
    '''

    '''

    def __init__(self, file_name: str, seed: int):
        self.core = NameSetCore()
        self.random = random.Random(8731 + seed)

        name_set = read_name_set_file(file_name)

        self.name_lists_dict = dict()
        for nl in self.core.name_lists:
            self.name_lists_dict[nl.tag] = nl



    def get_name(self) -> str:
        length = len(self.core.name_lists)
        name_list = self.core.name_lists[random.randrange(length)]
        length = len(name_list.names)
        return name_list.names[random.randrange(length)]

    def get_name_from_name_list_tag(self, name_list_tag: str) -> str:
        for name_list in self.core.name_lists:
            if name_list_tag == name_list.tag:
                # TODO: insert code to use markov chains when markov properties are present.
                length = len(name_list['names'])
                return name_list['names'][random.randrange(length)]

    def get_name_list_tags(self):
        for name_list in self.core.name_lists:
            yield name_list['tag']

    def add_names_to_namelist(self, names: list, name_list_tag: str):
        if name_list_tag in self.name_lists_dict:
            self.name_lists_dict[name_list_tag]['names'].append(names)
        else:
            raise Exception()

    def __repr__(self):
        return json.dumps(self.core.__dict__, indent='    ', ensure_ascii=False)

