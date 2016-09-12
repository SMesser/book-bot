from django.test import TestCase

from story.actions import TravelAction
from story.tests.actions.action_test_case import GenericActionTestMixin


class TravelTestCase(GenericActionTestMixin, TestCase):
	action_class = TravelAction
