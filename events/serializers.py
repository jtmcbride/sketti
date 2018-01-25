from rest_framework import serializers
from .models import Event, Group

class EventSerializer(serializers.ModelSerializer):
	# id = serializers.IntegerField(read_only=True)
	# title = serializers.CharField(max_length=255)
	# start_time = serializers.DateTimeField()
	# lat = models.FloatField()
	# lng = models.FloatField()
	# user = models.ForeignKey(User)
	# created_at = models.DateTimeField(auto_now_add=True)
	# updated_at = models.DateTimeField(auto_now=True)

	# def create(self, validated_data):
	# 	return Event.objects.create(**validated_data)

	# def update(self, instance, validated_data):
	# 	for key, val in validated_data:
	# 		instance.__dict__[key] = val : 
	# 	instance.title = validated_data.get('title', instance.title)
	# 	instance.start_time = validated_data.get('start_time')
	class Meta:
		model = Event
		fields = (
			'id',
			'title',
			'start_time',
			'lat',
			'lng',
			'user',
			'created_at',
			'updated_at'
		)

class GroupSerializer(serializers.ModelSerializer):

	class Meta:
		model = Group
		fields = (
			'id',
			'name',
			'description',
			'creator_id',
			'private',
			'created_at',
			'updated_at'
		)