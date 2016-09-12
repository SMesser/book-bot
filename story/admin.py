from django.contrib.admin import site

from story.models import Character, Group, Location, Title


site.register(Character)
site.register(Group)
site.register(Location)
site.register(Title)
