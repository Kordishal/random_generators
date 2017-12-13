from name_generator import *
import random

names = NameGeneration('/home/jonas/PycharmProjects/random_generators/name_generator/name_sets/', 82139)
names.load()
names.create_name_set_dict()

tags = names.all_tags
print(list(tags))

print('@@@ FULLY RANDOM NAMES @@@')
for _ in range(10):
    print(names.get_name())
print('@@@ TEMPLATE NAMES @@@')
for _ in range(10):
    print(names.generate_name_from_template(template="<building:building_type>"))

for _ in range(10):
    print(names.generate_name_from_set(name_set_tag='cities'))

for _ in range(10):
    print(names.generate_name_from_set(name_set_tag=random.choice(list(names.all_tags))))

for _ in range(100):
    print(names.generate_name_from_set('lakes'))

