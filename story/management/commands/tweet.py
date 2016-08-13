import tweepy
import secrets
import sys
from traceback import print_exc

from django.core.management.base import BaseCommand
from random import randint

from story.actions import ACTION_LIST


MAX_TWEET_LENGTH = 140
MAX_ESTIMATE_ACTION_LENGTH = 1
for action_class in ACTION_LIST:
	for verb in action_class.VERBS:
		if len(verb) >= MAX_ESTIMATE_ACTION_LENGTH:
			MAX_ESTIMATE_ACTION_LENGTH = len(verb)


class Command(BaseCommand):
	def handle(self, *args, **options):
		msg = ''
		parts = []
		while len(msg) + 2 < MAX_TWEET_LENGTH - MAX_ESTIMATE_ACTION_LENGTH:
			# Construct multiple sentences if we can do so while staying under
			# tweet length. This isn't guaranteed in either direction, but it's
			# a decent rough estimate.
			parts.append(self.construct_message())
			msg = '  '.join(parts)
		self.tweet(msg)

	def tweet(self, message):
		"""Post the given message."""
		auth = tweepy.OAuthHandler(secrets.consumer_key, secrets.consumer_secret)
		auth.set_access_token(secrets.access_token, secrets.access_token_secret)
		api = tweepy.API(auth)
		auth.secure = True
		print('Posting message "{}"'.format(message))
		# api.update_status(status=message)

	def choose_action_class(self):
		"""Choose a class of random DB actions."""
		action_weights = {
			action: action.weight_available()
			for action in ACTION_LIST
		}
		total_weight = sum(action_weights.values())
		item = randint(1, total_weight)
		for action_class, action_weight in action_weights.items():
			if action_weight < item:
				item -= action_weight
			else:
				return action_class
		return None

	def construct_message(self):
		"""Execute a random DB action and return a string describing it."""
		action_class = self.choose_action_class()
		if action_class is None:
			return 'Nothing much happened.'
		try:
			return action_class.execute()
		except Exception:
			print_exc(file=sys.stdout)
			mode = action_class.__name__.strip('Action').title()
			return 'Chaos raged across the universe of {}.'.format(mode)
