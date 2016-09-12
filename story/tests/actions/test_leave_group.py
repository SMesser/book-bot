from django.test import TestCase

from story.actions import LeaveGroupAction
from story.tests.actions.action_test_case import GenericActionTestMixin


class LeaveGroupTestCase(GenericActionTestMixin, TestCase):
	action_class = LeaveGroupAction
