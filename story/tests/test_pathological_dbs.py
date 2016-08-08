from story.models import Character, Group, Location, Title
from story.seed_data import CHARACTERS, GROUPS, LOCATIONS, TITLES
from story.tests.utils import StoryTestCase


class FullDBTests(StoryTestCase):
	"""Confirm database filled with all pre-gen records is sane.

	Tests are inherited from StoryTestCase.
	"""
	def setUp(self):
		for kwargs in CHARACTERS:
			Character.objects.create(**kwargs)
		for kwargs in GROUPS:
			Group.objects.create(**kwargs)
		for kwargs in LOCATIONS:
			Location.objects.create(**kwargs)
		for kwargs in TITLES:
			Title.objects.create(**kwargs)
