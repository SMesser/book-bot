from django.test import TestCase

from story.actions import ACTION_LIST


class GenericActionTests(TestCase):
	longMessage = True

	def extract_arguments_from_verb(self, verb):
		"""Utility to find the expected keyword arguments for formatting"""
		arguments = set()
		remainder = str(verb)
		while '{' in remainder:
			position = remainder.index('{')
			remainder = remainder[position + 1:]
			position = remainder.index('}')
			new_arg = remainder[:position]
			arguments.add(new_arg)
		return arguments

	def test_verb_structure(self):
		"""Check basic structure of each Action's VERBS constant"""
		for action_class in ACTION_LIST:
			expected_arguments = None
			for verb in action_class.VERBS:
				self.assertIsInstance(verb, basestring)
				if expected_arguments is None:
					expected_arguments = self.extract_arguments_from_verb(verb)
				else:
					self.assertEqual(
						expected_arguments,
						self.extract_arguments_from_verb(verb),
						msg='Inconsistent arguments for "{}" in {}'.format(
							verb,
							action_class
						)
					)

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
