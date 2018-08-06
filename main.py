from procedural_generators import NameGenerator
import random


if __name__ == '__main__':

    generator = NameGenerator('procedural_generators/data/name_sets/', seed=82139)

    ids = generator.name_set_ids()
    print(list(ids))

    print('@@@ FULLY RANDOM NAMES @@@')
    for _ in range(10):
        print(generator.generate())
    print('@@@ TEMPLATE NAMES @@@')
    for _ in range(10):
        print(generator.generate(template_name="english_male_full_name"))
    print('@@@ ENGLISH NAMES @@@')
    for _ in range(10):
        print(generator.generate(nameset_id='english_names'))

    print('@@@ NO ENGLISH NAMES @@@')
    for _ in range(10):
        print(generator.generate(tags=['english']))

    print('@@@ NO MALE NAMES @@@')
    for _ in range(10):
        print(generator.generate(tags=['male']))

    print('############ River Names ################')
    for _ in range(10):
        print(generator.generate(nameset_id='river_names'))

    print('############ Deity Names ################')
    for _ in range(10):
        print(generator.generate(template_name='mesopotamian_deity_name'))

    for _ in range(10):
        print(generator.generate(template_name='norse_male_deity_name'))

    for _ in range(10):
        print(generator.generate(template_name='norse_female_deity_name'))


