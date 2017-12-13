import json
import random

from json import JSONEncoder


class NameSetError(Exception):
    pass


class MissingTagError(NameSetError):

    def __init__(self, file_name, item_name):
        self.file_name = file_name
        self.item_name = item_name

    def __str__(self):
        return 'ERROR: The ' + self.item_name + ' in file ' + self.file_name + ' does not have a tag defined.'


class InvalidTemplateError(NameSetError):

    def __init__(self, name_set, missing_field):
        self.name_set = name_set
        self.missing_field = missing_field

    def __str__(self):
        return 'ERROR: A template in the name set ' + self.name_set + ' is invalid. You need to add a ' + self.missing_field + ' field.'


class InvalidNameListError(NameSetError):

    def __init__(self, name_set, missing_field):
        self.name_set = name_set
        self.missing_field = missing_field

    def __str__(self):
        return 'ERROR: A name list in the name set  ' + self.name_set + ' is invalid. You need to add a ' \
               + self.missing_field + ' field.'


class InvalidValueError(NameSetError):

    def __init__(self, name_set, field_name, encountered_type, expected_type):
        self.name_set = name_set
        self.field_name = field_name
        self.encountered_type = encountered_type
        self.expected_type = expected_type

    def __str__(self):
        return 'ERROR: In name set the field ' + self.field_name + ' was expected to be of type ' \
               + self.expected_type + ' but is of type ' + self.encountered_type + '.'


class NameTemplate(JSONEncoder):

    def __init__(self, template):
        super().__init__(ensure_ascii=False)
        try:
            self.name = template['name']
        except KeyError:
            self.name = ''
        try:
            self.content = template['content']
        except KeyError:
            raise InvalidTemplateError('', 'content')
        else:
            try:
                assert isinstance(self.content, str)
            except AssertionError:
                raise InvalidValueError('', 'content', str(type(self.content)), 'str')

        try:
            self.tags = template['tags']
        except KeyError:
            self.tags = None
        else:
            try:
                assert isinstance(self.tags, list)
            except AssertionError:
                raise InvalidValueError('', 'tags', str(type(self.tags)), 'list')
            else:
                for tag in self.tags:
                    try:
                        assert isinstance(tag, str)
                    except AssertionError:
                        raise InvalidValueError('', 'tag in tags', str(type(self.tags)), 'str')
        try:
            self.weight = template['weight']
        except KeyError:
            raise InvalidTemplateError('', 'weight[int]')
        else:
            try:
                assert isinstance(self.weight, int)
            except AssertionError:
                raise InvalidValueError('', 'weight', str(type(self.weight)), 'int')


class NameList(JSONEncoder):

    def __init__(self, name_list):
        super().__init__(ensure_ascii=False)
        try:
            self.name = name_list['name']
        except KeyError:
            self.name = ''
        try:
            self.tag = name_list['tag']
        except KeyError:
            raise NameSetError(attribute='tag')
        try:
            self.names = name_list['names']
        except KeyError:
            raise NameSetError(attribute='names')

        try:
            self.weight = name_list['weight']
        except KeyError:
            self.weight= 1
        try:
            self.use_markov = name_list['use_markov']
        except KeyError:
            self.use_markov = False
        if self.use_markov:
            try:
                self.markov_order = name_list['markov_order']
                self.markov_min_length = name_list['markov_min_length']
                self.markov_max_length = name_list['markov_max_length']
            except KeyError as ke:
                raise NameSetError(attribute=str(ke))


class NameSetCore(JSONEncoder):

    def __init__(self):
        super().__init__(ensure_ascii=False, default=self.default)
        self.tag = ''
        self.name = ''
        self.templates = list()
        self.name_lists = list()

    def default(self, o):
        templates = list()
        for template in self.templates:
            templates.append(template.__dict__)
        name_lists = list()
        for name_list in self.name_lists:
            name_lists.append(name_list.__dict__)
        return_value = dict()
        return_value['tag'] = self.tag
        return_value['name'] = self.name
        return_value['templates'] = templates
        return_value['name_lists'] = name_lists
        return return_value


class NameSet:
    '''

    '''
    def __init__(self, file_name, seed):
        self.core = NameSetCore()

        self.random = random.Random(8731 + seed)

        self.is_not_complete = False
        self.error_message = 'Namelist in file ' + str(file_name.split('/')[-1]) + ' has no {0}!'
        self.attribute_name = ''
        self.has_templates = False
        self.name_lists_dict = dict()
        self.read_name_set_file(file_name)

    def read_name_set_file(self, file_name: str) -> int:
        with open(file_name, 'r', encoding='utf-8-sig') as file:
            content = file.read()
            name_set = json.loads(content)

            try:
                self.core.name = name_set['name']
            except KeyError:
                self.core.name = ''

            try:
                self.core.tag = name_set['tag']
            except KeyError:
                self.error_message = 'The name_set in file ' + str(file_name.split('/')[-1]) + ' needs a tag!'
                print(self.error_message)
                self.is_not_complete = True
            try:
                assert self.core.tag != ''
            except AssertionError:
                self.error_message = 'The name_set in file ' + str(file_name.split('/')[-1]) + ' needs a tag which is not empty!'
                print(self.error_message)
                self.is_not_complete = True

            try:
                for template in name_set['templates']:
                    self.core.templates.append(NameTemplate(template))

                if len(self.core.templates) > 0:
                    self.has_templates = True
                else:
                    self.has_templates = False
            except KeyError:
                self.has_templates = False
                self.core.templates = None
            except InvalidTemplateError as invalid_template_error:
                raise InvalidTemplateError(self.core.tag, invalid_template_error.missing_field)

            self.core.name_lists = list()
            try:
                for name_list in name_set['name_lists']:
                    self.core.name_lists.append(NameList(name_list))
            except KeyError:
                self.error_message = 'Your name_set in file ' + str(file_name.split('/')[-1]) + \
                                     ' needs at least one name_list!'
                print(self.error_message)
                self.is_not_complete = True
            except NameSetError as inv:
                raise NameSetError(attribute=str(inv), name_set=self.core.tag)

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




