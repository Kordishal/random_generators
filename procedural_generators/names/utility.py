import os
import json
import re


class NameSetEditor(object):

    def __init__(self):
        self.name_sets = list()

    def load_file(self, file_name):
        with open(file_name, 'r', encoding='utf-8-sig') as file:
            self.name_sets.append(json.loads(file.read()))

    def load_all(self):
        for root, dirnames, files in os.walk('./'):
            for file in files:
                if not file.startswith('_') and file.endswith('.json'):
                    self.load_file(root + file)
        print('INFO: Loaded ' + str(len(self.name_sets)) + ' name sets.')

    def store(self):
        for name_set in self.name_sets:
            with open(name_set['tag'] + '.json', 'w', encoding='utf-8') as file:
                file.write(json.dumps(name_set, indent='    ', ensure_ascii=False))

    def change_tag(self, old_tag, new_tag):
        self.load_all()
        for name_set in self.name_sets:
            if name_set['tag'] == old_tag:
                name_set['tag'] = new_tag
            if 'templates' in name_set:
                for template in name_set['templates']:
                    template['content'] = re.sub(old_tag, new_tag, template['content'])
        try:
            os.remove('./' + old_tag + '.json')
        except FileNotFoundError:
            pass
        self.store()

    @staticmethod
    def add_tag(name_set, new_tag, level, default_value, condition=None):
        if level == 'name_set':
            if new_tag not in name_set:
                if condition is not None:
                    if condition(name_set):
                        name_set[new_tag] = default_value
                else:
                    name_set[new_tag] = default_value
        elif level == 'template':
            for template in name_set['templates']:
                if new_tag not in template:
                    if condition is not None:
                        if condition(template):
                            template[new_tag] = default_value
                    else:
                        template[new_tag] = default_value
        elif level == 'name_list':
            for name_list in name_set['name_lists']:
                if new_tag not in name_list:
                    if condition is not None:
                        if condition(name_list):
                            name_list[new_tag] = default_value
                    else:
                        name_list[new_tag] = default_value
        else:
            raise ValueError('Level needs to be either "name_set", "template" or "name_list". '
                             'No other values are accepted.')

    def add_tags_to_all(self, new_tag, level, default_value, condition=None):
        self.load_all()
        for name_set in self.name_sets:
            self.add_tag(name_set, new_tag, level, default_value, condition)
        self.store()

    def remove_tag(self, tag):
        self.load_all()
        for name_set in self.name_sets:
            for key in name_set:
                print(key)
                if key == tag:
                    del name_set[key]
                    print('INFO: Deleted ' + tag + ' in name set ' + name_set['tag'] + '.')
                    break
                elif key == 'templates':
                    for template in name_set['templates']:
                        for t in template:
                            if t == tag:
                                del template[t]
                                print('INFO: Deleted ' + tag + ' in a template.')
                                break
                elif key == 'name_lists':
                    for name_list in name_set['name_lists']:
                        for n in name_list:
                            if n == tag:
                                del name_list[n]
                                print('INFO: Deleted ' + tag + ' in name list ' + name_list['tag'] + '.')
                                break
        self.store()

    def remove_name_list(self, tag):
        self.load_all()
        for name_set in self.name_sets:
            for name_list in list(name_set['name_lists']):
                if name_list['tag'] == tag:
                    name_set['name_lists'].remove(name_list)
        self.store()

    def add_name_list_to_set(self, name_set_tag: str, name_list: dict):
        '''
        Adds a name list to a name set. Can add duplicates. Does not check if name list is a valid name list.

        :param name_set_tag: the name set the list should be added to. (str)
        :param name_list: the name list which should be added. (dict)
        '''
        self.load_all()
        for name_set in self.name_sets:
            if name_set['tag'] == name_set_tag:
                name_set['name_lists'].append(name_list)
        self.store()


if __name__ == '__main__':
    utility = NameSetEditor()
    # utility.change_tag('area_names', 'areas')
    # utility.add_tag('use_markov', 'name_list', True)
    # utility.remove_tag('markovproperties')


    def predicate(name_list):
        return True


    # utility.add_tags_to_all('weight', 'name_list', 10)

    utility.remove_name_list('full_real_world_names')

    with open('/home/jonas/PycharmProjects/random_generators/name_generator/data_files/lakes.json', 'r', encoding='utf-8') as file:
        content = file.read()
        utility.add_name_list_to_set('lakes', json.loads(content))
