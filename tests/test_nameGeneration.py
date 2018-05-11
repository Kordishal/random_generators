from unittest import TestCase
from name_generator import *
from random import Random
from name_generator.name_classes import InvalidTemplateError, InvalidValueError, InvalidNameListError, MissingTagError


class TestNameGeneration(TestCase):

    def setUp(self):
        self.names = NameGeneration('./test_name_sets/', 1)

    def test___init__(self):
        ng = NameGeneration('./test_name_sets/', 1002)
        self.assertEqual(ng.path, './test_name_sets/')

        with self.assertRaises(TypeError):
            NameGeneration(192, 1)

        with self.assertRaises(OSError):
            NameGeneration('./test_names/', 1000)

        self.assertIsInstance(ng.random, Random)
        self.assertIsInstance(ng.name_set_dict, dict)
        self.assertIsInstance(ng.name_sets, list)

    def test_load_all(self):
        self.names.load_all()
        self.assertEqual(len(self.names.name_sets), len(self.names.all_tags))

        for sets in self.names.name_sets:
            self.assertFalse(sets.is_not_complete)

    def test_load_file(self):
        self.names.load_file('./test_name_sets/hill_range_names.json')

