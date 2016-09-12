from django.test import TestCase

from story.actions import GroupCreationAction
from story.tests.actions.action_test_case import GenericActionTestMixin


class GroupCreationTestCase(GenericActionTestMixin, TestCase):
	action_class = GroupCreationAction
