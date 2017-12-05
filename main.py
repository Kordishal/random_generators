import name_generator


names = name_generator.NameGeneration()
names.load_default()
names.make_keys_lowercase()

names.write_to_namesets()