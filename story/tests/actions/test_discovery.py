from django.test import TestCase

from story.actions import DiscoveryAction
from story.tests.actions.action_test_case import GenericActionTestMixin


class DiscoveryTestCase(GenericActionTestMixin, TestCase):
	action_class = DiscoveryAction
