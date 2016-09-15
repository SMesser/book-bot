from django.test import TestCase

from story.actions import TravelAction
from story.models import Character
from story.tests.actions.action_test_case import GenericActionTestMixin
from story.tests.factories import CharacterFactory, LocationFactory


class TravelTestCase(GenericActionTestMixin, TestCase):
	action_class = TravelAction

	def test_single_location_blocks_motion(self):
		"""If there is only one location, characters can't travel"""
		place = LocationFactory()
		CharacterFactory(location=place)
		self.assertEqual(self.action_class.weight_available(), 0)

	def test_travel_predictable_with_single_character_and_two_locations(self):
		"""If there is only one location, characters can't travel"""
		old_place, new_place = LocationFactory.create_batch(2)
		char = CharacterFactory(location=old_place)
		self.action_class.get_kwargs()
		char = Character.objects.get(pk=char.pk)
		self.assertEqual(char.location, new_place)
