from django.contrib.admin import helpers
from django.contrib.admin.util import quote, unquote
from django.forms.formsets import all_valid
from django.core.exceptions import ValidationError, PermissionDenied
from django.core.urlresolvers import reverse
from django.http.response import Http404
from django.utils.encoding import force_text
from inei.enssec.models import Pais, Continente, Consulado

__author__ = 'holivares'
IS_POPUP_VAR = '_popup'

from django.contrib import admin
from django.contrib.admin.views.main import ChangeList


class PaisAdmin(admin.ModelAdmin):
    list_display = ('id', 'continente', 'nombre', 'nombreOficial', 'capital')
    list_per_page = 15


class ContinenteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    list_per_page = 15


class ConsuladoChangeList(ChangeList):
    def url_for_result(self, result):
        pk = getattr(result, self.pk_attname)
        continente = result.continente.id
        pk = '%s-%s' % (pk, continente)
        return reverse('admin:%s_%s_change' % (self.opts.app_label,
                                               self.opts.model_name),
                       args=(quote(pk),),
                       current_app=self.model_admin.admin_site.name)


class ConsuladoAdmin(admin.ModelAdmin):
    list_display = ('id', 'continente', 'nombre')
    list_per_page = 15
    list_display_links = ('nombre', )

    def get_object(self, request, object_id):
        """
        Returns an instance matching the primary key provided. ``None``  is
        returned if no match is found (or the object_id failed validation
        against the primary key field).
        """
        _pk = object_id.split('-')
        consulado = _pk[0]
        continente = _pk[1]
        queryset = self.get_queryset(request)
        model = queryset.model
        try:
            return queryset.get(pk=consulado, continente=continente)
        except (model.DoesNotExist, ValidationError, ValueError):
            return None

    def get_changelist(self, request, **kwargs):
        """
        Returns the ChangeList class for use on the changelist page.
        """
        return ConsuladoChangeList

    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        """
        if change:
            self.model.objects.filter(id=obj.id, continente=obj.continente).update(
                nombre = obj.nombre
            )
        else:
            obj.save()

admin.site.register(Pais, PaisAdmin)
admin.site.register(Continente, ContinenteAdmin)
admin.site.register(Consulado, ConsuladoAdmin)