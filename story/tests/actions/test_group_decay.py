from django.test import TestCase

from story.actions import GroupDecayAction
from story.tests.actions.action_test_case import GenericActionTestMixin


class GroupDecayTestCase(GenericActionTestMixin, TestCase):
	action_class = GroupDecayAction
