from django.test import TestCase

from story.actions import GroupSpreadAction
from story.tests.actions.action_test_case import GenericActionTestMixin


class GroupSpreadTestCase(GenericActionTestMixin, TestCase):
	action_class = GroupSpreadAction
