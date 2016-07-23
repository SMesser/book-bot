from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Character(models.Model):
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
	name = models.TextField(unique=True)
	gender = models.SmallIntegerField(choices=GENDERS)
	location = models.ForeignKey(
		'story.Location',
		null=True,
		blank=True,
		default=None
	)


class Office(models.Model):
	class Meta:
		unique_together = (('group', 'title'),)

	officer = models.ForeignKey('story.Character')
	group = models.ForeignKey('story.Group')
	title = models.ForeignKey('story.Title')


class Group(models.Model):
	name = models.TextField(unique=True)


class Location(models.Model):
	name = models.TextField(unique=True)


class Title(models.Model):
	name = models.TextField(unique=True)
