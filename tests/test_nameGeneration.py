from unittest import TestCase
from name_generator import *


class TestNameGeneration(TestCase):

    def setUp(self):
        self.names = NameGeneration(1)

    def test_set_path(self):
        path = '/home/jonas/PycharmProjects/random_generators/name_generator/name_sets/'
        self.names.set_path('/home/jonas/PycharmProjects/random_generators/name_generator/name_sets/')
        self.assertEquals(path, self.names.path)
        self.assertTrue(self.names.valid_path)

        self.names.path = ''
        self.names.valid_path = False

        path = '/hmsid/asc8/ksjd'
        self.names.set_path(path)
        self.assertEquals('', self.names.path)
        self.assertFalse(self.names.valid_path)

        with self.assertRaises(TypeError):
            self.names.set_path(None)
        self.assertEquals('', self.names.path)
        self.assertFalse(self.names.valid_path)



        self.names.set_path(11)


    def test_load(self):
        self.names.set_path('/home/jonas/PycharmProjects/random_generators/name_generator/name_sets/')
        self.names.load()
        self.assertIsNotNone(self.names.name_sets)
        self.assertGreaterEqual(1, len(self.names.name_sets))