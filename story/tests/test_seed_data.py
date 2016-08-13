from collections import Sequence
from django.test import TestCase

from story.seed_data import CHARACTERS, GROUPS, LOCATIONS, TITLES

DATA_LISTS = [CHARACTERS, GROUPS, LOCATIONS, TITLES]


class SeedDataTests(TestCase):
	def test_data_structure(self):
		"""Confirm consistency and format of seed data lists"""
		for data_list in DATA_LISTS:
			expected_keys = None
			self.assertIsInstance(data_list, Sequence)
			for variant in data_list:
				self.assertIsInstance(variant, dict)
				if expected_keys is None:
					expected_keys = set(variant.keys())
					for key in expected_keys:
						self.assertIsInstance(key, basestring)
				else:
					self.assertEqual(expected_keys, set(variant.keys()))
