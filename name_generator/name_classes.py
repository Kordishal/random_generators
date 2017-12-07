import json
import random


class NameSet:

    def __init__(self, file_name, seed):
        self.random = random.Random(8731 + seed)
        self.is_not_complete = False
        self.error_message = 'Namelist in file ' + str(file_name.split('/')[-1]) + ' has no {0}!'
        self.attribute_name = ''
        self.name = ''
        self.tag = ''
        self.has_templates = False
        self.templates = list()
        self.name_lists = list()
        self.name_lists_dict = dict()
        self.read_name_set_file(file_name)

    def read_name_set_file(self, file_name: str) -> int:
        with open(file_name, 'r', encoding='utf-8-sig') as file:
            content = file.read()
            name_set = json.loads(content)

            try:
                self.name = name_set['name']
            except KeyError:
                self.name = ''

            try:
                self.tag = name_set['tag']
            except KeyError:
                self.error_message = 'The name_set in file ' + str(file_name.split('/')[-1]) + ' needs a tag!'
                print(self.error_message)
                self.is_not_complete = True
            try:
                assert self.tag != ''
            except AssertionError:
                self.error_message = 'The name_set in file ' + str(file_name.split('/')[-1]) + ' needs a tag which is not empty!'
                print(self.error_message)
                self.is_not_complete = True

            try:
                for template in name_set['templates']:
                    self.templates.append(dict(template))
                    try:
                        assert template['content']
                    except AssertionError:
                        self.error_message = 'One of your templates in file ' + str(file_name.split('/')[-1]) + \
                                             ' has no content (or it is misspelled...).'
                        print(self.error_message)
                        self.is_not_complete = True
                    try:
                        assert template['weight']
                    except AssertionError:
                        self.error_message = 'One of your templates in file ' + str(file_name.split('/')[-1]) + \
                                             ' has no weight (or it is misspelled...).'
                        print(self.error_message)
                        self.is_not_complete = True
                if len(self.templates) > 0:
                    self.has_templates = True
                else:
                    self.has_templates = False
            except KeyError:
                self.has_templates = False
                self.templates = None

            self.name_lists = list()
            try:
                for name_list in name_set['name_lists']:
                    self.name_lists.append(dict(name_list))
                    try:
                        assert name_list['tag']
                    except AssertionError:
                        self.error_message = 'One of your name_lists in file ' + str(file_name.split('/')[-1]) + \
                                             ' has no tag (or it is misspelled...).'
                        print(self.error_message)
                        self.is_not_complete = True
                    try:
                        assert len(name_list['names']) > 0
                    except (AssertionError, KeyError) as err:
                        if isinstance(err, AssertionError):
                            self.error_message = 'Your name_list ' + name_list['tag'] + ' in name set ' + self.name + \
                                                 ' needs at least one name in names (or it is misspelled...).'
                        if isinstance(err, KeyError):
                            self.error_message = 'Your name_list ' + name_list['tag'] + ' in name set ' + self.name + \
                                                 ' needs names (or it is misspelled...).'
                        print(self.error_message)
                        self.is_not_complete = True

                    if 'markov_properties' in name_list:
                        if name_list['markov_properties'] is not None:
                            try:
                                assert name_list['markov_properties']['length']
                                assert name_list['markov_properties']['order']
                            except AssertionError:
                                self.error_message = 'Your name_list ' + name_list['tag'] + ' in name set ' + self.name + \
                                         ' markov_properties needs a value "length" and "order". At least one of them is ' \
                                         'missing or misspelled.'
                                print(self.error_message)
                                self.is_not_complete = True
            except KeyError:
                self.error_message = 'Your name_set in file ' + str(file_name.split('/')[-1]) + \
                                     ' needs at least one name_list!'
                print(self.error_message)
                self.is_not_complete = True

            self.name_lists_dict = dict()
            for nl in self.name_lists:
                self.name_lists_dict[nl['tag']] = nl

            for name_list in self.name_lists:
                try:
                    assert name_list['names']
                    assert len(name_list['names']) > 0
                except AssertionError:
                    try:
                        name_list_tag = name_list.tag
                    except AttributeError:
                        name_list_tag = 'unknown'
                    self.is_not_complete = True
                    self.attribute_name = 'name_lists.names with tag ' + name_list_tag

            if self.is_not_complete:
                print(self.error_message.format(self.attribute_name))

    def get_name(self) -> str:
        length = len(self.name_lists)
        name_list = self.name_lists[random.randrange(length)]
        length = len(name_list['names'])
        return name_list['names'][random.randrange(length)]

    def get_name_from_name_list_tag(self, name_list_tag: str) -> str:
        for name_list in self.name_lists:
            if name_list_tag == name_list.tag:
                # TODO: insert code to use markov chains when markov properties are present.
                length = len(name_list['names'])
                return name_list['names'][random.randrange(length)]

    def get_name_list_tags(self):
        for name_list in self.name_lists:
            yield name_list['tag']

    def __repr__(self):
        return json.dumps(self.__dict__, indent='    ', ensure_ascii=False)




