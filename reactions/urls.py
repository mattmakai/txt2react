from django.conf.urls import *

from .views import (EventsListView, CreateEventView, EventDetailView, )

urlpatterns = patterns('reactions.views',
    # just make the reactions list the 'dashboard' for the moment, later
    # we can snaz this up
    url(r'reactions/list/$', EventsListView.as_view(), 
        name='dashboard'),

    url(r'events/list/$', EventsListView.as_view(), 
        name='reactions_list'),
    url(r'event/new/$', CreateEventView.as_view(), name="create_event"),
    url(r'event/view/(?P<slug>[a-zA-Z0-9\-]+)/$', EventDetailView.as_view(), 
        name="view_event"),
    url(r'event/feedback/', 'respond_to_msg', name='respond_to_msg'),
)

