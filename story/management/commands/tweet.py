import tweepy # for tweeting
import secrets # shhhh
import sys
from traceback import print_exc

from django.core.management.base import BaseCommand
from random import choice

from story.models import Character, Location


class Command(BaseCommand):
	def __init__(self):
		super(Command, self).__init__()
		self.mode_methods = {
			'travel': self.construct_travel_message
		}

	def handle(self, *args, **options):
		msg = self.construct_message()
		self.tweet(msg)

	def tweet(self, message):
		auth = tweepy.OAuthHandler(secrets.consumer_key, secrets.consumer_secret)
		auth.set_access_token(secrets.access_token, secrets.access_token_secret)
		api = tweepy.API(auth)
		auth.secure = True
		print("Posting message {}".format(message))
		api.update_status(status=message)

	def construct_message(self):
		mode = choice(self.mode_methods.keys())
		try:
			message = self.mode_methods[mode]()
		except Exception:
			message = 'Chaos raged across the universe of {}'.format(mode)
			print_exc(file=sys.stdout)
		else:
			if message is None:
				message = 'Nothing much happened'
		return message

	def construct_travel_message(self):
		if Location.objects.exists() and Character.objects.exists():
			active_char = choice(list(Character.objects.all()))
			if active_char.location is None:
				new_location = choice(list(Location.objects.all()))
				active_char.location = new_location
				active_char.save()
				return '{} arrived at {}'.format(
					active_char.name,
					new_location.name
				)
			elif Location.objects.exclude(id=active_char.location.id).exists():
				old_location = active_char.location
				new_location = choice(list(Location.objects.exclude(
					id=old_location.id
				)))
				active_char.location = new_location
				active_char.save()
				return '{} traveled from {} to {}'.format(
					active_char.name,
					old_location.name,
					new_location.name
				)
			else:
				return '{} remained in {}'.format(
					active_char.name,
					active_char.location.name
				)
