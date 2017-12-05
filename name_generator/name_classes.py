import json


class NameSet:

    def __init__(self, file_name):

        with open(file_name, 'r', encoding='utf-8-sig') as file:
            content = file.read()
            name_set = json.loads(content)

            try:
                self.name = name_set['name']
            except KeyError:
                self.name = name_set['Name']

            try:
                self.tag = name_set['tag']
            except KeyError:
                self.tag = name_set['Tag']

            self.templates = list()
            try:
                for template in name_set['templates']:
                    self.templates.append(dict(template))
            except KeyError:
                for template in name_set['Templates']:
                    self.templates.append(dict(template))

            self.name_lists = list()
            try:
                for name_list in name_set['name_lists']:
                    self.name_lists.append(dict(name_list))
            except KeyError:
                for name_list in name_set['NameLists']:
                    self.name_lists.append(dict(name_list))

    def __repr__(self):
        return json.dumps(self.__dict__, indent='    ', ensure_ascii=False)


