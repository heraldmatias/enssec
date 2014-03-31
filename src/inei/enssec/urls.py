from inei.enssec.models import TotalDigitacionConsulado

__author__ = 'holivares'

from django.conf.urls import patterns, url
from inei.enssec.views import (IndexView, CuestionarioView, SignOut, TotalDigitacionListView, TotalDigitacionConsuladoListView,
                               ResumenDigitacionListView, AdminView, CuestionarioDetailView, CuestionarioAjaxView)

urlpatterns = patterns('',
                       url(r'^$', IndexView.as_view(), name='index'),
                       url(r'^cuestionario/$', CuestionarioView.as_view(), name='cuestionario1'),
                       url(r'^cuestionario/(?P<pk>\d+)/$', CuestionarioDetailView.as_view(), name='cuestionario-view'),
                       url(r'^cuestionario/ajax/$', CuestionarioAjaxView.as_view(), name='cuestionario-ajax'),
                       url(r'^cuestionario/admin/$', AdminView.as_view(), name='cuestionario-admin'),
                       url(r'^cuestionario/total/$', TotalDigitacionListView.as_view(), name='cuestionario-total'),
                       url(r'^cuestionario/resumen/$', ResumenDigitacionListView.as_view(), name='cuestionario-resumen'),
                       url(r'^cuestionario/total/consulado/$', TotalDigitacionConsuladoListView.as_view(),
                           name='cuestionario-total-consulado'),
                       url(r'^logout/$', SignOut.as_view(), name='logout'),
)