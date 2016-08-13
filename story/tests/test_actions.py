from django.test import TestCase

from story.actions import ACTION_LIST


class GenericActionTests(TestCase):
	longMessage = True

	def extract_arguments_from_verb(self, verb):
		"""Utility to find the expected keyword arguments for formatting"""
		raise NotImplementedError

	def test_verb_structure(self):
		"""Check basic structure of each Action's VERBS constant"""
		expected_arguments = None
		for action_class in ACTION_LIST:
			for verb in action_class.VERBS:
				self.assertIsInstance(verb, basestring)

	def test_verb_terminators(self):
		"""Confirm every sentence ends with proper punctuation"""
		verb_terminators = '.'
		for action_class in ACTION_LIST:
			for verb in action_class.VERBS:
				self.assertIn(
					verb[-1],
					verb_terminators,
					msg='{} verb "{}" does not end in an allowed character'.format(
						action_class.__name__,
						verb
					)
				)
