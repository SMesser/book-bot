from django.test import TestCase

from story.management.commands.tweet import ACTION_LIST


class StoryTestCase(TestCase):
	"""Superclass for testing with custom asserts and basic structural tests.

	Since this class has an empty setUp(), it confirms an empty database is
	sane.
	"""

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
