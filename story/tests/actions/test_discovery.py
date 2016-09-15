from django.test import TestCase

from story.actions import DiscoveryAction
from story.models import Location
from story.seed_data import LOCATIONS
from story.tests.actions.action_test_case import GenericActionTestMixin
from story.tests.factories import LocationFactory


class DiscoveryTestCase(GenericActionTestMixin, TestCase):
	action_class = DiscoveryAction

	def test_no_remaining_locations_means_no_discovery(self):
		"""If all pre-generated locations exist, don't make more"""
		for loc_kwargs in LOCATIONS:
			Location.objects.create(**loc_kwargs)
		self.assertEqual(self.action_class.weight_available(), 0)

	def test_do_not_re_create_existing_location(self):
		"""Existing Locations should not be re-discovered."""
		place = LocationFactory()
		self.assertNotEqual(
			self.action_class.get_kwargs()['place'],
			place.name.title()
		)

	def test_get_kwargs_makes_location(self):
		"""get_kwargs() should instantiate the Location"""
		new_place_name = self.action_class.get_kwargs()['place']
		self.assertEqual(
			new_place_name,
			Location.objects.get().name.title()
		)
