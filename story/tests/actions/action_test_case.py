from story.actions import ACTION_LIST


class GenericActionTestMixin(object):
	longMessage = True
	action_class = None

	@staticmethod
	def extract_arguments_from_verb(verb):
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
		expected_arguments = None
		for verb in self.action_class.VERBS:
			self.assertIsInstance(verb, basestring)
			if expected_arguments is None:
				expected_arguments = self.extract_arguments_from_verb(verb)
			else:
				self.assertEqual(
					expected_arguments,
					self.extract_arguments_from_verb(verb),
					msg='Inconsistent arguments for "{}" in {}'.format(
						verb,
						self.action_class
					)
				)

	def test_verb_terminators(self):
		"""Confirm every sentence ends with proper punctuation"""
		verb_terminators = '.'
		for verb in self.action_class.VERBS:
			self.assertIn(
				verb[-1],
				verb_terminators,
				msg='{} verb "{}" does not end in an allowed character'.format(
					self.action_class.__name__,
					verb
				)
			)

	def test_action_class_in_action_list(self):
		"""Confirm this class of action is available"""
		self.assertIn(self.action_class, ACTION_LIST)
