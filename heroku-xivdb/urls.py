from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

import dviews.views

urlpatterns = patterns('',
    url(r'^slacklookup/$', dviews.views.slack, name='slack')
)
