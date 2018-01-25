# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
# from django.contrib.auth.models import User

# Create your models here.	
class Group(models.Model):

	name = models.CharField(max_length=128)
	description = models.TextField(default='')
	creator = models.ForeignKey(settings.AUTH_USER_MODEL)
	private = models.BooleanField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		db_table = "groups"
		verbose_name = "Group"
		verbose_name_plural = "Groups"

	# def __str__(self):
	# 	return "Group: {0}" % self.name


class GroupMembership(models.Model):

	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	group = models.ForeignKey(Group)
	active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	deleted_at = models.DateTimeField(null=True, blank=True)

	class Meta:
		db_table = "group_memberships"
		verbose_name = "GroupMembership"
		verbose_name_plural = "GroupMemberships"

	def __str__(self):
		return "User {0} to Group {1}".format(self.user_id, self.group_id)


class EventManager(models.Manager):

	def by_user_id(self, user_id):
		query = """
			SELECT events.* FROM
				events
			JOIN
				groups g ON g.id=events.group_id
			JOIN 
				group_memberships gm on gm.group_id=g.id
			WHERE
				gm.user_id=%s
		"""
		result = self.raw(query, (user_id,))
		return result

class Event(models.Model):
	
	title = models.CharField(max_length=255)
	start_time = models.DateTimeField()
	lat = models.FloatField()
	lng = models.FloatField()
	group = models.ForeignKey(Group)
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


	objects = EventManager()

	class Meta:
		db_table = "events"
		verbose_name = "Event"
		verbose_name_plural = "Events"

	def __str__(self):
		return "{0} @ {1} created by User {2}".format(self.title, self.start_time, self.user_id)

class Vote(models.Model):

	upvote = models.BooleanField()
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	event = models.ForeignKey(Event)

	class Meta:
		db_table = "votes"
		unique_together = (('user', 'event'))
		verbose_name = "Vote"
		verbose_name_plural = "Votes"

	def __str__(self):
		return "Vote: {0} by {1}".format(self.upvote, self.user_id)
