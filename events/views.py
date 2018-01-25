# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# from django.shortcuts import render
from django.http import JsonResponse, Http404
from django.contrib.auth import authenticate, login, logout, get_user_model

from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated, APIException

from .models import Event
from .serializers import EventSerializer

# Create your views here.
@api_view(['GET', 'POST'])	
# @renderer_classes((JSONRenderer,))
def events(request):
	"""Fetch events by user or create events"""
	user_id = request.user.id
	if request.method == "POST":
		event = Event.objects.create(user_id=user_id, **request.data)
		serial = EventSerializer(event)
	else:
		user_events = Event.objects.filter(user_id=user_id)
		serial = EventSerializer(user_events, many=True)

	return Response(serial.data)

@api_view(['PATCH', 'DELETE'])
@renderer_classes((JSONRenderer,))
def edit_event(request, id):
	event = Event.objects.filter(id=id).update(**request.data)
	Event.objects.get(id)
	if event:
		import pdb ; pdb.set_trace()
		serial = EventSerializer(event)
		return Response(serial.data)
	else:
		raise Http404()

@api_view(['GET'])	
# @renderer_classes((BrowsableAPIRenderer,))
def user_events(request):
	if request.user.is_authenticated():
		user_id = request.user.id
		user_events = Event.objects.filter(user_id=user_id)
		serial = EventSerializer(user_events, many=True)

		return Response(serial.data)
		
	else:
		raise NotAuthenticated(code=401)

@api_view(['POST'])
def login_user(request):
	"""Log in user through AJAX"""
	if request.user.is_authenticated():
		raise APIException("User is already logged in")
	username = request.data.get("username")
	password = request.data.get("password")
	user = authenticate(username=username, password=password)
	if user is not None:
		login(request, user)
		return Response()
	raise AuthenticationFailed()


@api_view(['DELETE'])
def logout_user(request):
	"""AJAX logout"""
	if request.user.is_authenticated():
		logout(request)
		return Response()
	raise APIException("User is not logged in")


@api_view(['POST'])
def create_user(request):
	"""AJAX user creation"""
	User = get_user_model()
	username = request.data['username']
	password = request.data['password']
	new_user = User.objects.create_user(username, password=password)
	login(request, new_user)
	return Response(status=201)

class EventList(APIView):
	"""List events"""

	def get(self, request):
		user_id = request.user.id

		user_events = Event.objects.filter(user_id=user_id)
		serial = EventSerializer(user_events, many=True)

		return Response(serial.data)

	def post(self, request):
		pass
	
	def put(self, request):
		pass