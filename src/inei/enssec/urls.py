__author__ = 'holivares'

from django.conf.urls import patterns, url
from inei.enssec.views import (IndexView, CuestionarioView)

urlpatterns = patterns('',
                       url(r'^$', IndexView.as_view(), name='index'),
                       url(r'^cuestionario/$', CuestionarioView.as_view(), name='cuestionario1'),)