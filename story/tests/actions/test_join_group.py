from django.test import TestCase

from story.actions import JoinGroupAction
from story.tests.actions.action_test_case import GenericActionTestMixin
from story.tests.factories import (
	CharacterFactory,
	GroupFactory,
	LocationFactory
)


class JoinGroupTestCase(GenericActionTestMixin, TestCase):
	action_class = JoinGroupAction

	def test_empty_database_implies_zero_weight(self):
		"""Confirm an empty database has zero weight for this action."""
		self.assertEqual(self.action_class.weight_available(), 0)

	def test_characters_without_groups_implies_zero_weight(self):
		"""A characters with no Group gives zero weight."""
		new_place = LocationFactory()
		CharacterFactory(location=new_place)
		self.assertEqual(self.action_class.weight_available(), 0)

	def test_no_characters_implies_zero_weight(self):
		"""A location with no character gives zero weight."""
		new_group = GroupFactory()
		new_place = LocationFactory()
		new_group.influences.add(new_place)
		self.assertEqual(self.action_class.weight_available(), 0)

	def test_only_char_at_group_location_in_group_implies_zero_weight(self):
		"""Can't add existing members to a group"""
		place = LocationFactory()
		group = GroupFactory()
		char = CharacterFactory(location=place)
		group.members.add(char)
		group.influences.add(place)
		self.assertEqual(self.action_class.weight_available(), 0)

	def test_character_not_at_group_location_implies_zero_weight(self):
		"""Can't join a distant group"""
		char_place, group_place = LocationFactory.create_batch(2)
		group = GroupFactory()
		CharacterFactory(location=char_place)
		group.influences.add(group_place)
		self.assertEqual(self.action_class.weight_available(), 0)

	def test_nonmember_at_group_location_single_choice(self):
		"""Can join a local group"""
		place = LocationFactory()
		group = GroupFactory()
		CharacterFactory(location=place)
		group.influences.add(place)
		self.assertEqual(self.action_class.weight_available(), 1)

	def test_nonmember_at_group_location_yields_predicted_choice(self):
		"""Acceptable character can join local group"""
		place = LocationFactory()
		group = GroupFactory()
		char, member = CharacterFactory.create_batch(2, location=place)
		group.influences.add(place)
		group.members.add(member)
		self.assertEqual(
			self.action_class.get_kwargs(),
			{
				'character': char.name,
				'group': group.name
			}
		)

	def test_nonmember_at_group_location_yields_predicted_choice(self):
		"""Acceptable character can join local group"""
		place = LocationFactory()
		group = GroupFactory()
		char = CharacterFactory(location=place)
		group.influences.add(place)
		self.action_class.get_kwargs()
		self.assertEqual(
			{char},
			set(group.members.all())
		)
