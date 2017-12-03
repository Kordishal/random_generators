import json


class NameSet:

    def __init__(self, file_name):
        with open(file_name, 'r', encoding='utf-8') as file:
            content = ''
            for line in file:
                content += line
            name_set = json.loads(content)

            self.name = name_set['Name']
            self.tag = name_set['Tag']
            self.templates = list()

            for template in name_set['Templates']:
                self.templates.append(dict(template))
            self.name_lists = list()
            for name_list in name_set['Names']:
                self.name_lists.append(dict(name_list))

    def __repr__(self):
        return json.dumps(self.__dict__, indent='    ', ensure_ascii=False)


