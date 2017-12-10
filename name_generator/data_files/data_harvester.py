import json
import csv
import re
from name_generator.name_classes import NameSet


class HarvestData:

    def __init__(self):
        self.names = dict()

    def load_data(self):
        self.names['lakes'] = list()
        with open('Lake.csv', 'r') as file:
            reader = csv.DictReader(file, dialect='unix')
            count = 0
            for row in reader:
                count += 1
                if count > 3:
                    if row['rdf-schema#label'] != 'NULL':
                        self.names['lakes'].append(row['rdf-schema#label'])
            print(count)
        print(len(self.names['lakes']))

        self.names['lakes_single'] = list()

        for i in range(len(self.names['lakes'])):
            self.names['lakes'][i] = re.sub('\(.*?\)', '', self.names['lakes'][i])
            self.names['lakes'][i] = self.names['lakes'][i].strip()
            if not self.names['lakes_single'].__contains__(self.names['lakes'][i]):
                self.names['lakes_single'].append(self.names['lakes'][i])

        self.names['lakes'] = self.names['lakes_single']
        del self.names['lakes_single']

        with open('lakes.json', 'w', encoding='utf-8') as file:
            file.write(json.dumps(self.names, indent='    ', ensure_ascii=False))

    def write_data_into_name_set(self, name_set_tag: str, name_list_tag: str):
        name_set = NameSet(name_set_tag, 1)
        name_set.add_names_to_namelist(self.names[name_set_tag], name_list_tag)


harvester = HarvestData()
harvester.load_data()
harvester.write_data_into_name_set('we are many', 'stuff')



