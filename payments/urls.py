from django.conf.urls.defaults import *

urlpatterns = patterns('payments.views',
    url(r'^home/purchased/(?P<uid>\d+)/(?P<id>\d+)/$', 'purchased'), # callback
    url(r'^pay/$', 'stripePayment'),
    url(r'^receipt/(?P<pid>[0-9]+)/$', 'receipt', name='receipt'),
)
