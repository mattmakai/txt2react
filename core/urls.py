from django.conf.urls import *

from .views import (LandingView, LoginView, AboutView, LearnMoreView, 
                    ContactView, SignUpView, )


urlpatterns = patterns('core.views',
    url(r'^sign-in/$', LoginView.as_view(), name='signin'),
    url(r'^sign-up/$', SignUpView.as_view(), name='signup'),
    url(r'^logout/$', 'signout', name='signout'),
    url(r'^contact/$', ContactView.as_view(), name='contact'),
    url(r'^about/$', AboutView.as_view(), name='about'),
    url(r'^learn-more/$', LearnMoreView.as_view(), name='learn_more'),
    url(r'^generate-customer-profile/$', 'generate_customer_profile',
        name='generate_customer_profile'),
    url(r'^$', LandingView.as_view(), name='landing'),
)

