from unittest import TestCase
from name_generator.name_sets.util import NameSetUtility


class TestNameSetUtility(TestCase):

    def setUp(self):
        self.utility = NameSetUtility()

    def test___init__(self):
        self.assertIsInstance(self.utility.name_sets, list)

    def test_load_file(self):
        self.utility.load_file('./test_name_sets/hill_range_names.json')
        self.assertEqual(len(self.utility.name_sets), 1)
        self.assertIsInstance(self.utility.name_sets[0], dict)