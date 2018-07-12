import os
import random

from random_names.name_set import NameSet
from random_names.exceptions import UnknownNameList, UnknownNameSet, UnknownTemplate


class NameGenerator(object):
    """

    :param data_folder:
    :param seed:
    """

    def __init__(self, data_folder='name_data/', seed=102932):
        self._random = random.Random(seed)
        self.name_sets = dict()
        for root, dirs, files in os.walk(data_folder):
            for file in files:
                name_set = NameSet(root + file, seed)
                self.name_sets[name_set.id] = name_set
                seed += 1

    @property
    def templates(self):
        result = dict()
        for nameset in self.name_sets:
            for template in self.name_sets[nameset].templates:
                result[template] = self.name_sets[nameset].templates[template]
        return result

    @property
    def name_sets_as_list(self):
        return list(self.name_sets.values())

    def name_set_ids(self):
        return [nameset.id for nameset in self.name_sets.values()]

    def generate(self, nameset_id=None, template_name=None, tags=None):

        if template_name is not None:
            template = self.templates.get(template_name, None)
            if template is not None:
                return template.expand(self.name_sets)
            else:
                raise UnknownTemplate('The template %s could not be found!' % template_name)

        if nameset_id is None:
            name_set = self.select_name_set(tags)
        else:
            try:
                name_set = self.name_sets[nameset_id]
            except KeyError:
                raise UnknownNameSet('No name set with id %s was found!' % nameset_id)

        template = self._random.choice(name_set.filter_templates(tags))
        return template.expand(self.name_sets)

    def select_name_set(self, tags):
        def _contains(l_name_set: NameSet):
            templates = l_name_set.templates_as_list

            for tag in tags:
                for temp in l_name_set.templates_as_list:
                    if tag in temp.tags:
                        templates.remove(temp)

            if len(templates) > 0:
                return True
            else:
                return False
        if tags is not None:
            namesets = list(filter(_contains, self.name_sets_as_list))
        else:
            namesets = list(self.name_sets.values())

        return self._random.choice(namesets)



