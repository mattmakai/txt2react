from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('core.urls')),
    url(r'^', include('reactions.urls')),

    # third party applications
    url(r'', include('social_auth.urls')),

    # django admin
    url(r'^admin/', include(admin.site.urls)),
)

# this should only be used for deploying to Heroku without a CDN
urlpatterns += patterns('django.contrib.staticfiles.views',
    url(r'^static/(?P<path>.*)$', 'serve'),
)
