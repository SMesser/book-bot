from random import choice

from story.models import Character, Location
from story.seed_data import CHARACTERS, LOCATIONS, TITLES


def create_from_seed_list(model, seed_list):
	if model.objects.count() >= len(seed_list):
		raise ValueError('Cannot make more {} records.'.format(model.name))
	created = False
	while not created:
		kwargs = choice(seed_list)
		record, created = model.objects.get_or_create(**kwargs)
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
		'went',
		'drove',
		'flew',
		'walked',
		'traveled'
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
		text = '{} {} from {} to {}.'.format(
			character.name,
			verb,
			character.location.name,
			location.name
		)
		character.location = location
		character.save()
		return text


class CharacterCreationAction(Action):
	VERBS = [
		'arrived at',
		'drove to',
		'flew to',
		'walked to',
		'traveled to',
		'materialized at',
		'appeared at',
		'was discovered at',
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
		return '{} {} {}.'.format(
			character.name,
			verb,
			character.location.name,
		)


class DiscoveryAction(Action):
	VERBS = [
		'was discovered',
		'materialized',
		'appeared'
	]

	@classmethod
	def weight_available(cls):
		if Location.objects.count() > len(LOCATIONS):
			return 1
		else:
			return 0

	@classmethod
	def execute(cls):
		verb = choice(cls.VERBS)
		location = create_from_seed_list(Location, LOCATIONS)
		return '{} {}.'.format(
			location.name.title(),
			verb
		)
