import tweepy
import secrets
import sys
from traceback import print_exc

from django.core.management.base import BaseCommand
from random import randint

from story.actions import (
	CharacterCreationAction,
	DiscoveryAction,
	GroupCreationAction,
	TravelAction
)


ACTION_LIST = [
	CharacterCreationAction,
	DiscoveryAction,
	GroupCreationAction,
	TravelAction,
]


class Command(BaseCommand):
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
		action_weights = {
			action: action.weight_available()
			for action in ACTION_LIST
		}
		total_weight = sum(action_weights.values())
		item = randint(0, total_weight)
		for action_class, action_weight in action_weights.items():
			if action_weight < item:
				item -= action_weight
			else:
				try:
					return action_class.execute()
				except Exception:
					print_exc(file=sys.stdout)
					mode = action_class.__class__.__name__.strip('Action').lower()
					return 'Chaos raged across the universe of {}.'.format(mode)
		return 'Nothing much happened'
