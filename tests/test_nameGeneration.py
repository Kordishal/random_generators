from unittest import TestCase
from name_generator import *


class TestNameGeneration(TestCase):

    def setUp(self):
        self.names = NameGeneration(1)