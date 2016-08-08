from __future__ import unicode_literals

from django.db.models import (
	ForeignKey,
	ManyToManyField,
	Model,
	SmallIntegerField,
	TextField
)


class Character(Model):
	MALE = -1
	NEUTER = 0
	FEMALE = 1
	OTHER = 2
	MUFTALE = 3

	GENDERS = (
		(MALE, 'Male'),
		(FEMALE, 'Female'),
		(NEUTER, 'Neuter'),
		(MUFTALE, 'Muftale'),
		(OTHER, 'Varies / Other')
	)
	name = TextField(unique=True)
	gender = SmallIntegerField(choices=GENDERS)
	location = ForeignKey(
		'story.Location',
		null=True,
		blank=True,
		default=None
	)


class Office(Model):
	class Meta:
		unique_together = (('group', 'title'),)

	officer = ForeignKey('story.Character')
	group = ForeignKey('story.Group')
	title = ForeignKey('story.Title')


class Group(Model):
	name = TextField(unique=True)
	influences = ManyToManyField('story.Location')
	members = ManyToManyField('story.Character')


class Location(Model):
	name = TextField(unique=True)


class Title(Model):
	name = TextField(unique=True)
