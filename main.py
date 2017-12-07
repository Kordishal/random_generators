from name_generator import *
import random

names = NameGeneration()
names.load_default()
names.create_name_set_dict()
# names.make_keys_lowercase()
# names.write_to_namesets()

tags = names.name_set_tags()
print(list(tags))

print('@@@ FULLY RANDOM NAMES @@@')
for i in range(10):
    print(names.get_name())
print('@@@ TEMPLATE NAMES @@@')
for i in range(10):
    print(names.generate_name_from_template(template="<building:building_type>"))

for i in range(10):
    print(names.generate_name_from_set(name_set_tag='cities'))

for i in range(10):
    print(names.generate_name_from_set(name_set_tag=random.choice(list(names.name_set_tags()))))

for i in range(100):
    print(names.generate_name_from_set('lakes'))

