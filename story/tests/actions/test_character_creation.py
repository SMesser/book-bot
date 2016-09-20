from django.test import TestCase

from story.actions import CharacterCreationAction
from story.models import Character
from story.seed_data import CHARACTERS
from story.tests.actions.action_test_case import GenericActionTestMixin
from story.tests.factories import LocationFactory


class CharacterCreationTestCase(GenericActionTestMixin, TestCase):
	action_class = CharacterCreationAction

	def test_no_characters_made_gives_positive_weight(self):
		"""Must be able to create characters when none are present."""
		LocationFactory()
		self.assertGreaterEqual(self.action_class.weight_available(), 1)

	def test_no_locations_made_gives_zero_weight(self):
		"""Must NOT be able to create characters when there are no places."""
		self.assertEqual(self.action_class.weight_available(), 0)

	def test_all_pregen_characters_made_gives_zero_weight(self):
		"""Only Create new characters as long as seed data is available."""
		place = LocationFactory()
		for char_kwargs in CHARACTERS:
			Character.objects.create(location=place, **char_kwargs)
		self.assertEqual(self.action_class.weight_available(), 0)

	def test_single_location_predicts_reported_location(self):
		"""get_kwargs() must report the single available location"""
		place = LocationFactory()
		self.assertEqual(
			str(self.action_class.get_kwargs()['place']),
			str(place)
		)

	def test_single_location_predicts_character_location(self):
		"""get_kwargs() puts new characters at the single available location"""
		place = LocationFactory()
		self.action_class.get_kwargs()
		char = Character.objects.get()
		self.assertEqual(char.location, place)
