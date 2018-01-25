from django.conf.urls import url

from . import views

app_name = 'events'

urlpatterns = [
	url(r'^login', views.login_user),
	url(r'^logout', views.logout_user),
	url(r'^user', views.create_user),
	url(r'^events/(?P<id>[0-9]{1,9})/', views.edit_event),
	# url(r'^events/$', views.events),
	url(r'^events/$', views.EventList.as_view()),
	url(r'^user/events', views.user_events),
]