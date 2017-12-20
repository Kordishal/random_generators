import json
import random

from json import JSONEncoder


class NameSetError(Exception):
    pass


class MissingTagError(NameSetError):
    pass


class InvalidTemplateError(NameSetError):

    def __init__(self, missing_field):
        self.missing_field = missing_field


class InvalidNameListError(NameSetError):

    def __init__(self, missing_field):
        self.missing_field = missing_field


class NoNameListError(NameSetError):
    pass


class InvalidValueError(NameSetError):

    def __init__(self, field_name, encountered_type='', expected_type='', value=''):
        self.field_name = field_name
        self.encountered_type = encountered_type
        self.expected_type = expected_type
        self.value = value


class UnexpectedFieldError(NameSetError):

    def __init__(self, field_name):
        self.field_name = field_name


class NameTemplate(JSONEncoder):

    def __init__(self, template):
        super().__init__(ensure_ascii=False)
        for key in template:
            if key == 'name':
                self.name = template['name']
            elif key == 'content':
                self.content = template['content']
            elif key == 'tags':
                self.tags = template['tags']
            elif key == 'weight':
                self.weight = template['weight']
            else:
                raise UnexpectedFieldError(key)

        if hasattr(self, 'name'):
            if not isinstance(self.name, str):
                raise InvalidValueError('name', encountered_type=str(type(self.name)), expected_type='str')

        if hasattr(self, 'content'):
            if not isinstance(self.content, str):
                raise InvalidValueError('content', encountered_type=str(type(self.content)), expected_type='str')
        else:
            raise InvalidTemplateError('content')

        if hasattr(self, 'tags'):
            if not isinstance(self.tags, list):
                raise InvalidValueError('tags', encountered_type=str(type(self.tags)), expected_type='list')
            else:
                if not len(self.tags) > 0:
                    raise InvalidTemplateError('tags')

        if hasattr(self, 'weight'):
            if not isinstance(self.weight, int):
                raise InvalidValueError('weight', encountered_type=str(type(self.weight)), expected_type='int')
        else:
            raise InvalidTemplateError('weight')


class NameList(JSONEncoder):

    def __init__(self, name_list):
        super().__init__(ensure_ascii=False)
        for key in name_list:
            if key == 'name':
                self.name = name_list['name']
            elif key == 'tag':
                self.tag = name_list['tag']
            elif key == 'names':
                self.names = name_list['names']
            elif key == 'weight':
                self.weight = name_list['weight']
            elif key == 'use_markov':
                self.use_markov = name_list['use_markov']
            elif key == 'markov_order':
                self.markov_order = name_list['markov_order']
            elif key == 'markov_min_length':
                self.markov_min_length = name_list['markov_min_length']
            elif key == 'markov_max_length':
                self.markov_max_length = name_list['markov_max_length']
            else:
                raise UnexpectedFieldError(key)

        if not hasattr(self, 'tag'):
            raise InvalidTemplateError('tag')
        elif not isinstance(self.tag, str):
            raise InvalidValueError('tag', encountered_type=str(type(self.tag)),
                                    expected_type='str')
        if hasattr(self, 'name'):
            if not isinstance(self.name, str):
                raise InvalidValueError('name', encountered_type=str(type(self.name)),
                                        expected_type='str')
        if hasattr(self, 'names'):
            if not isinstance(self.names, list):
                raise InvalidNameListError('names')
            elif len(self.names) == 0:
                raise InvalidNameListError('names')
        else:
            raise InvalidNameListError('names')

        if hasattr(self, 'weight'):
            if not isinstance(self.weight, int):
                raise InvalidValueError('weight', encountered_type=str(type(self.weight)),
                                        expected_type='int')
        else:
            raise InvalidNameListError('weight')
        if hasattr(self, 'use_markov'):
            if not isinstance(self.use_markov, bool):
                raise InvalidValueError('use_markov', encountered_type=str(type(self.use_markov)),
                                        expected_type='bool')
            elif self.use_markov:
                if not isinstance(self.markov_order, int):
                    raise InvalidValueError('markov_order', encountered_type=str(type(self.markov_order)),
                                            expected_type='int')
                if not isinstance(self.markov_max_length, int):
                    raise InvalidValueError('markov_max_length', encountered_type=str(type(self.markov_max_length)),
                                            expected_type='int')
                if not isinstance(self.markov_min_length, int):
                    raise InvalidValueError('markov_min_length', encountered_type=str(type(self.markov_min_length)),
                                            expected_type='int')


class NameSetCore(JSONEncoder):

    def __init__(self):
        super().__init__(ensure_ascii=False, default=self.default)

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

    def __init__(self, file_name: str, seed: int):
        self.core = NameSetCore()
        self.random = random.Random(8731 + seed)
        self.has_templates = False

        self.read_name_set_file(file_name)

        self.name_lists_dict = dict()
        for nl in self.core.name_lists:
            self.name_lists_dict[nl.tag] = nl

    def read_name_set_file(self, file_name: str):
        with open(file_name, 'r', encoding='utf-8-sig') as file:
            content = file.read()
            name_set = json.loads(content)
            for key in name_set:
                if key == 'name':
                    self.core.name = name_set['name']
                elif key == 'tag':
                    self.core.tag = name_set['tag']
                elif key == 'templates':
                    if isinstance(name_set[key], list):
                        self.core.templates = list()
                        for item in name_set[key]:
                            try:
                                template = NameTemplate(item)
                            except InvalidTemplateError as err:
                                raise err
                            except InvalidValueError as err:
                                raise err
                            except UnexpectedFieldError as err:
                                raise err
                            else:
                                self.core.templates.append(template)
                        if len(self.core.templates) > 0:
                            self.has_templates = True
                elif key == 'name_lists':
                    if isinstance(name_set[key], list):
                        self.core.name_lists = list()
                        for item in name_set[key]:
                            try:
                                name_list = NameList(item)
                            except InvalidNameListError as err:
                                raise err
                            except InvalidValueError as err:
                                raise err
                            except UnexpectedFieldError as err:
                                raise err
                            else:
                                self.core.name_lists.append(name_list)
                else:
                    raise UnexpectedFieldError(key)

            if hasattr(self.core, 'tag'):
                if not isinstance(self.core.tag, str):
                    raise InvalidValueError('tag', encountered_type=str(type(self.core.tag)), expected_type='str')
            else:
                raise MissingTagError()

            if hasattr(self.core, 'name_lists'):
                if not isinstance(self.core.name_lists, list):
                    raise InvalidValueError('name_list', encountered_type=str(type(self.core.name_lists)), expected_type='list')
            else:
                raise NoNameListError()

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




