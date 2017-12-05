from name_generator.name_classes import NameSet
import os


class NameGeneration:

    def __init__(self):
        self.name_sets = list()
        self.path = "/home/jonas/PycharmProjects/random_generators/name_generator/name_sets/"

    def load_default(self):
        for root, dir, files in os.walk(self.path):
            for file in files:
                self.name_sets.append(NameSet(root + file))

    def write_to_namesets(self):
        for i in self.name_sets:
            with open(self.path + i.tag + '.json', 'w') as file:
                file.write(str(i))

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


