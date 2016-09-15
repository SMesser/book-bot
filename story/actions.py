from django.db.models import Count
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


def get_related_model_from_through_model(through, fieldname):
	"""Get model class referenced by a through model's field"""
	field_attr = getattr(through, fieldname).field
	try:
		return field_attr.related_model
	except AttributeError:
		# Handle older versions of Django's non-public API
		return field_attr.related.parent_model


def create_from_through_table(through, field1, field2):
	"""Create and return a random new record for a through table

	Inefficient if the through table is near fully-populated. Assumes there are
	not-yet-instantiated relationships.
	"""

	model1 = get_related_model_from_through_model(through, field1)
	model2 = get_related_model_from_through_model(through, field2)
	created = False
	while not created:
		arg1 = model1.objects.order_by('?')[0]
		arg2 = model2.objects.order_by('?')[0]
		record, created = through.objects.get_or_create(
			**{field1: arg1, field2:arg2}
		)
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
		kwargs = cls.get_kwargs()
		verb = choice(cls.VERBS)
		return verb.format(**kwargs)

	@classmethod
	def get_kwargs(cls):
		"""Determine the records involved in the action and update them.

		Returns a dictionary of keyword arguments to format <cls>.VERBS.
		"""
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
			Character.objects.filter(location__isnull=False).count() * (Location.objects.count() - 1),
			0
		)

	@classmethod
	def get_kwargs(cls):
		character = Character.objects.filter(location__isnull=False).order_by(
			'?'
		)[0]
		location = Location.objects.exclude(id=character.location.id).order_by(
			'?'
		)[0]
		origin = character.location.name
		character.location = location
		character.save()
		return {
			'character': character.name,
			'origin': origin,
			'destination': location.name,
		}


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
		if Character.objects.count() <= len(CHARACTERS):
			return min([
				Location.objects.count(),
				7,
				len(CHARACTERS) - Character.objects.count()
			])
		else:
			return 0

	@classmethod
	def get_kwargs(cls):
		character = create_from_seed_list(Character, CHARACTERS)
		character.location = Location.objects.order_by('?')[0]
		character.save()
		return {
			'character': character.name,
			'place': character.location.name,
		}


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
	def get_kwargs(cls):
		location = create_from_seed_list(Location, LOCATIONS)
		return {'place': location.name.title()}


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
	def get_kwargs(cls):
		group = create_from_seed_list(Group, GROUPS)
		location = Location.objects.order_by('?')[0]
		group.influences.add(location)
		return {'group': group.name, 'place': location.name}


class GroupSpreadAction(Action):
	VERBS = [
		'{group} gained influence in {place}.',
		'{place} fell under the sway of {group}.',
	]

	@classmethod
	def weight_available(cls):
		return min(
			7,
			Group.objects.count() * Location.objects.count() -\
				Group.influences.through.objects.count(),
		)

	@classmethod
	def get_kwargs(cls):
		influence = create_from_through_table(
			Group.influences.through,
			'group',
			'location'
		)
		return {
			'group': influence.group.name,
			'place': influence.location.name
		}


class GroupDecayAction(Action):
	VERBS = [
		'{group} lost influence in {place}.',
		'{group} left {place}.',
	]

	@classmethod
	def weight_available(cls):
		return Group.influences.through.objects.count()

	@classmethod
	def get_kwargs(cls):
		influence = Group.influences.through.objects.order_by('?')[0]
		influence.delete()
		return {
			'group': influence.group.name,
			'place': influence.location.name
		}


class JoinGroupAction(Action):
	VERBS = [
		'{character} was inducted into {group}.',
		'{group} recruited {character}.',
		'{character} joined {group}.',
	]

	@classmethod
	def find_possible_joins(cls):
		"""Find possible Join-Group Locations

		Character must be in a place where the group has influence to join the
		group.
		"""

		annotated_locations = Location.objects.annotate(
			num_char=Count('character'),
			num_group=Count('group')
		)
		join_locations = set(annotated_locations.filter(
			num_char__gte=1,
			num_group__gte=1
		))

		# Restrict join_locations if all characters there belong to all groups
		# at that location. Copy the set so that we don't edit the set over
		# which we iterate.
		for loc in set(join_locations):
			possible_characters = set(loc.character_set.all())
			location_groups = set(loc.group_set.all())
			for char in set(possible_characters):
				possible_groups = location_groups - set(char.group_set.all())
				if len(possible_groups) == 0:
					possible_characters.remove(char)
			if len(possible_characters) == 0:
				join_locations.remove(loc)
		return join_locations

	@classmethod
	def weight_available(cls):
		return min(7, len(cls.find_possible_joins()))

	@classmethod
	def get_kwargs(cls):
		event_location = choice(list(cls.find_possible_joins()))
		possible_characters = set(event_location.character_set.all())
		location_groups = set(event_location.group_set.all())
		for char in set(possible_characters):
			possible_groups = location_groups - set(char.group_set.all())
			if len(possible_groups) == 0:
				possible_characters.remove(char)
		character = choice(list(possible_characters))
		group = choice(list(location_groups - set(character.group_set.all())))
		group.members.add(character)
		return {
			'character': character.name,
			'group': group.name
		}


class LeaveGroupAction(Action):
	VERBS = [
		'{character} retired from {group}.',
		'{group} expelled {character}.',
		'{character} left {group}.'
	]

	@classmethod
	def weight_available(cls):
		return min(
			7,
			Group.members.through.objects.count()
		)

	@classmethod
	def get_kwargs(cls):
		membership = Group.members.through.objects.order_by('?')[0]
		membership.delete()
		return {
			'character': membership.character.name,
			'group': membership.group.name
		}


ACTION_LIST = [
	CharacterCreationAction,
	DiscoveryAction,
	GroupCreationAction,
	GroupDecayAction,
	GroupSpreadAction,
	JoinGroupAction,
	LeaveGroupAction,
	TravelAction,
]
