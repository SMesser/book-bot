from random import choice

from story.models import Character, Group, Location, Title
from story.seed_data import CHARACTERS, GROUPS, LOCATIONS, TITLES


def create_from_seed_list(model, seed_list):
	"""Pick one dict of kwargs from a static list and instantiate it."""
	if model.objects.count() >= len(seed_list):
		raise ValueError('Cannot make more {} records.'.format(model.name))

	# Make a copy of the original list. Remove items from the duplicate list as
	# we try them. This prevents repeated attempts at duplicates and speeds
	# finding new kwargs if seed_list is large.
	remaining = list(seed_list)
	created = False
	while not created:
		kwargs = choice(seed_list)
		record, created = model.objects.get_or_create(**kwargs)
		remaining.remove(kwargs)
	return record


class Action(object):
	"""Broadly-structured actions that may happen"""

	@classmethod
	def weight_available(cls):
		"""Given DB state, estimate number of possibilities for this action"""
		return 0

	@classmethod
	def execute(cls):
		"""Update database and return a string to be tweeted."""
		raise NotImplementedError


class TravelAction(Action):
	VERBS = [
		'{character} went from {origin} to {destination}.',
		'{character} drove from {origin} to {destination}.',
		'{character} flew from {origin} to {destination}.',
		'{character} walked from {origin} to {destination}.',
		'{character} traveled from {origin} to {destination}.',
		'{character} moved from {origin} to {destination}.',
	]

	@classmethod
	def weight_available(cls):
		return max(
			Character.objects.filter(location__isnull=True).count() * (Location.objects.count() - 1),
			0
		)

	@classmethod
	def execute(cls):
		character = Character.objects.order_by('?')[0]
		location = Location.objects.exclude(id=character.location.id).order_by('?')[0]
		verb = choice(cls.VERBS)
		text = verb.format(
			character=character.name,
			origin=character.location.name,
			destination=location.name,
		)
		character.location = location
		character.save()
		return text


class CharacterCreationAction(Action):
	VERBS = [
		'{character} arrived at {place}.',
		'{character} drove to {place}.',
		'{character} flew to {place}.',
		'{character} walked to {place}.',
		'{character} traveled to {place}.',
		'{character} materialized at {place}.',
		'{character} appeared at {place}.',
		'{character} was discovered at {place}.',
	]

	@classmethod
	def weight_available(cls):
		if Character.objects.count() > len(CHARACTERS):
			return Location.objects.count()
		else:
			return 0

	@classmethod
	def execute(cls):
		character = create_from_seed_list(Character, CHARACTERS)
		character.location = Location.objects.order_by('?')[0]
		character.save()
		verb = choice(cls.VERBS)
		return verb.format(
			character=character.name,
			place=character.location.name,
		)


class DiscoveryAction(Action):
	VERBS = [
		'{place} was discovered.',
		'{place} materialized.',
		'{place} appeared.'
	]

	@classmethod
	def weight_available(cls):
		if len(LOCATIONS) > Location.objects.count():
			return 1
		else:
			return 0

	@classmethod
	def execute(cls):
		verb = choice(cls.VERBS)
		location = create_from_seed_list(Location, LOCATIONS)
		return verb.format(place=location.name.title())


class GroupCreationAction(Action):
	VERBS = [
		'The {group} arose at {place}.',
		'{place} was the birthplace of {group}.',
	]

	@classmethod
	def weight_available(cls):
		if not Location.objects.exists():
			return 0
		if len(GROUPS) > Group.objects.count():
			return 1
		else:
			return 0

	@classmethod
	def execute(cls):
		group = create_from_seed_list(Group, GROUPS)
		location = Location.objects.order_by('?')[0]
		verb = choice(cls.VERBS)
		return verb.format(group=group.name, place=location.name)
