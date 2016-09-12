from django.test import TestCase

from story.actions import CharacterCreationAction
from story.tests.actions.action_test_case import GenericActionTestMixin


class CharacterCreationTestCase(GenericActionTestMixin, TestCase):
	action_class = CharacterCreationAction
