from django.conf.urls import *

from .views import (ReactionsListView,)

urlpatterns = patterns('reactions.views',
    # just make the reactions list the 'dashboard' for the moment, later
    # we can snaz this up
    url(r'reactions/list/$', ReactionsListView.as_view(), 
        name='dashboard'),

    url(r'reactions/list/$', ReactionsListView.as_view(), 
        name='reactions_list'),
)

