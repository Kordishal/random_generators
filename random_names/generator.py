import os
import random

from random_names.name_set import NameSet
from random_names.exceptions import InvalidTemplateError

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

    def name_set_ids(self):
        return [nameset.id for nameset in self.name_sets.values()]

    def generate(self, nameset_id=None, template_name=None, tags=None):

        if template_name is not None:
            template = self.templates.get(template_name, None)
            if template is not None:
                return template.expand(self.name_sets)
            else:
                raise InvalidTemplateError('The template %s could not be found!' % template_name)

        if nameset_id is None:
            name_set = self.select_name_set(tags)
        else:
            name_set = self.name_sets[nameset_id]

        template = self._random.choice(list(name_set.templates.values()))
        return template.expand(self.name_sets)

    def select_name_set(self, tags):

        def _contains(name_set: NameSet):
            for tag in tags:
                if tag in name_set.tags():
                    return False
            return True

        if tags is not None:
            namesets = list(filter(_contains, list(self.name_sets.values())))
        else:
            namesets = list(self.name_sets.values())

        return self._random.choice(namesets)


