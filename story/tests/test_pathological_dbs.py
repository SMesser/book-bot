from django.test import TestCase

from story.management.commands.tweet import ACTION_LIST
from story.models import Character, Group, Location, Title
from story.seed_data import CHARACTERS, GROUPS, LOCATIONS, TITLES


class StoryTestCase(TestCase):
	"""Superclass for testing with custom asserts and basic structural tests.

	Since this class has an empty setUp(), it confirms an empty database is
	sane.
	"""
	longMessage = True

	def assertWeightsNonnegative(self):
		"""Assert all weights are non-negative."""
		for action_class in ACTION_LIST:
			weight = action_class.weight_available()
			self.assertGreaterEqual(weight, 0)
			self.assertIsInstance(weight, int)

	def assertSomeActionPossible(self):
		"""Confirm the sum of weights is positive."""
		self.assertGreater(
			sum([
				action_class.weight_available()
				for action_class in ACTION_LIST
			]),
			0
		)

	def test_setup_database_consistent(self):
		"""Whatever the initial database is, confirm no negative weights"""
		self.assertWeightsNonnegative()

	def test_some_action_possible(self):
		"""Whatever the initial database is, confirm some action is available"""
		self.assertSomeActionPossible()

	def test_spot_check_actions(self):
		for action_class in ACTION_LIST:
			if action_class.weight_available() > 0:
				self.assertIsInstance(
					action_class.get_kwargs(),
					dict,
					msg='Failure for {}'.format(action_class.__name__)
				)


class FullDBTests(StoryTestCase):
	"""Confirm database filled with all pre-gen records is sane.

	Test methods are inherited from StoryTestCase.
	"""

	def setUp(self):
		for kwargs in CHARACTERS:
			Character.objects.create(**kwargs)
		for kwargs in GROUPS:
			Group.objects.create(**kwargs)
		for kwargs in LOCATIONS:
			Location.objects.create(**kwargs)
		for kwargs in TITLES:
			Title.objects.create(**kwargs)
