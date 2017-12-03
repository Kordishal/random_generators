from name_classes import NameSet
import os

name_sets = list()

base_path = "name_sets/"

for root, dirs, files in os.walk(base_path):
    for file in files:
        name_sets.append(NameSet(root + file))

print(name_sets)