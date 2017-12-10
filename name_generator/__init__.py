from name_generator.name_classes import NameSet
import os
import random
import re


class NameGeneration:

    def __init__(self, seed):
        self.name_sets = list()
        self.name_set_dict = dict()
        self.current_name_set_tag = ''
        self.path = ''
        self.valid_path = False

        self.all_tags = []

        self.random = random.Random(seed)

    def set_path(self, path: str):
        # raise a type error if path is not a string or None.
        if not isinstance(path, str) and not path:
            print('This is not a valid path name: ' + str(path))
            return -1
        if not os.path.exists(path):
            raise IOError('Path ' + path + ' does not exist.')

        self.path = path
        self.valid_path = True

    def load(self):
        """
        Load all name sets found in @self.path
        :return:
        """
        for root, dirnames, files in os.walk(self.path):
            for file in files:
                if not file.startswith('_') and file.endswith('.json'):
                    self.name_sets.append(NameSet(root + file, self.random.randint(0, 10000)))
        for name_set in self.name_sets:
            if name_set.is_not_complete:
                print('[WARNING] The name set "' + name_set.name + '" was removed as it was not complete. (err-msg: ' +
                      name_set.error_message)
                self.name_sets.remove(name_set)

        for name_set in self.name_sets:
            self.all_tags.append(name_set.tag)

    def write(self):
        for root, dirnames, files in os.walk(self.path):
            for file in files:
                if not file.startswith('_') and file.endswith('.json'):
                    os.remove(root + file)
        for i in self.name_sets:
            with open(self.path + i.tag + '.json', 'w') as file:
                file.write(str(i))

    def create_name_set_dict(self):
        for ns in self.name_sets:
            self.name_set_dict[ns.core.tag] = ns

    def get_name(self) -> str:
        if len(self.name_sets) > 0:
            return self.name_sets[self.random.randrange(len(self.name_sets))].get_name()
        else:
            print("No name sets loaded.")

    def get_name_from_list(self, name_list) -> str:
        length = len(name_list.names)
        name = name_list.names[self.random.randrange(length)]
        return name

    def get_name_from_template_part(self, template_part: str) -> str:
        template_part = template_part.strip('<>')
        try:
            name_set_tag, name_list_tag = template_part.split(':')
        except ValueError:
            name_set_tag = self.current_name_set_tag
            name_list_tag = template_part
        for ns in self.all_tags:
            if ns == name_set_tag:
                name_set = self.name_set_dict[ns]
                for nl in name_set.get_name_list_tags():
                    if nl == name_list_tag:
                        name_list = name_set.name_lists_dict[nl]
                        return self.get_name_from_list(name_list)

    def generate_name_from_template(self, template):
        matches = re.findall('<.*?>', template)
        for match in matches:
            try:
                template = template.replace(match, self.get_name_from_template_part(match))
            except TypeError as tp:
                print('ERROR: ' + str(tp) + ' in ' + self.current_name_set_tag + ' with template ' + template)
        return template

    def generate_name_from_set(self, name_set_tag):
        try:
            name_set = self.name_set_dict[name_set_tag]
        except KeyError:
            print('Nameset with tag "' + name_set_tag + '" does not exist.')
            return ''

        try:
            assert name_set.core.templates is not None
        except AssertionError:
            print('Nameset with tag "' + name_set_tag + '" does not have templates.')
            return ''
        self.current_name_set_tag = name_set_tag

        total_weight = 0
        for template in name_set.core.templates:
            total_weight += template.weight

        chance = self.random.randrange(total_weight)
        prev = 0
        current = 0
        for template in name_set.core.templates:
            current += template.weight
            if prev <= chance < current:
                return self.generate_name_from_template(template.content)
            prev = current

    def make_keys_lowercase(self):
        for name_set in self.name_sets:
            for template in name_set.templates:
                for key in template:
                    template[key.lower()] = template.pop(key)

            for name_list in name_set.name_lists:
                for key in name_list:
                    name_list[key.lower()] = name_list.pop(key)

                    if isinstance(name_list[key], dict):
                        for key_2 in name_list[key]:
                            name_list[key][key_2.lower()] = name_list[key].pop(key_2)


