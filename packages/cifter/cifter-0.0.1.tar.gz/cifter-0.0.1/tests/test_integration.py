from unittest import TestCase
from cifter import parse_file


class TestIntegration(TestCase):

    def test_from_file(self):
        document = parse_file("tests/data/ttisf760.mca")
