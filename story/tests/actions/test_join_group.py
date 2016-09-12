from django.test import TestCase
from random import choice

from story.actions import JoinGroupAction
from story.models import Character, Group, Location
from story.seed_data import CHARACTERS, GROUPS, LOCATIONS
from story.tests.actions.action_test_case import GenericActionTestMixin


class JoinGroupTestCase(GenericActionTestMixin, TestCase):
	action_class = JoinGroupAction

	def test_empty_database_implies_zero_weight(self):
		"""Confirm an empty database has zero weight for this action."""
		self.assertEqual(self.action_class.weight_available(), 0)

	def test_characters_without_groups_implies_zero_weight(self):
		"""A characters with no Group gives zero weight."""
		new_place = Location.objects.create(**choice(LOCATIONS))
		Character.objects.create(
			location=new_place,
			**choice(CHARACTERS)
		)
		self.assertEqual(self.action_class.weight_available(), 0)

	def test_no_characters_implies_zero_weight(self):
		"""A location with no character gives zero weight."""
		new_group = Group.objects.create(**choice(GROUPS))
		new_place = Location.objects.create(**choice(LOCATIONS))
		new_group.influences.add(new_place)

		self.assertEqual(self.action_class.weight_available(), 0)
