from django.test import TestCase

from story.management.commands.tweet import ACTION_LIST


class GenericActionTests(TestCase):
	def extract_arguments_from_verb(self, verb):
		raise NotImplementedError

	def test_verb_structure(self):
		"""Check basic structure of each Action's VERBS constant"""
		exected_arguments = None
		for action_class in ACTION_LIST:
			for verb in action_class.VERBS:
				self.assertIsInstance(verb, basestring)
