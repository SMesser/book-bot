from factory import DjangoModelFactory, Faker
from factory.fuzzy import FuzzyChoice

from story.models import Character, Group, Location, Office, Title


GENDER_CHOICES = [number for number, name in Character.GENDERS]


class CharacterFactory(DjangoModelFactory):
	class Meta:
		model = Character

	name = Faker('name')
	gender = FuzzyChoice(GENDER_CHOICES)


class GroupFactory(DjangoModelFactory):
	class Meta:
		model = Group

	name = Faker('company')


class LocationFactory(DjangoModelFactory):
	class Meta:
		model = Location

	name = Faker('name')


class OfficeFactory(DjangoModelFactory):
	class Meta:
		model = Office


class TitleFactory(DjangoModelFactory):
	class Meta:
		model = Title

	name = Faker('bs')
