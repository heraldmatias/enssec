from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import FormView, TemplateView
from django.http.response import HttpResponseRedirect, HttpResponse
from django.views.generic.base import RedirectView
from django.views.generic.list import ListView
from inei.auth.forms import LoginForm
from django.contrib.auth import login, authenticate, logout
import json
from inei.enssec.forms import CuestionarioForm, TotalDigitacionForm, ResumenDigitacionForm
from inei.enssec.models import Cuestionario, Consulado, Continente, Pais, UsuarioConsulado, \
    TotalDigitacion, ResumenDigitacion

__author__ = 'holivares'


class SignOut(RedirectView):

    permanent = False
    query_string = True

    def get_redirect_url(self):
        logout(self.request)
        return reverse('index')


class IndexView(FormView):
    template_name = 'index.html'
    form_class = LoginForm

    def form_valid(self, form):
        username = form.data['username']
        password = form.data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                #print self.request.user
                id = user.id or 0
                login(self.request, user)
                return HttpResponseRedirect(self.get_success_url())
            else:
                #cuenta deshabilitada
                return self.render_to_response(self.get_context_data(form=form))
        else:
            #login invalido
            return self.render_to_response(self.get_context_data(form=form))

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates a blank version of the form.
        """
        if request.user.is_authenticated():
            return redirect(self.get_success_url())
        return super(IndexView, self).get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('cuestionario1')


class CuestionarioView(FormView):
    template_name = 'cuestionario/cuestionario.html'
    form_class = CuestionarioForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if UsuarioConsulado.objects.filter(usuario=self.request.user).exists():
            pre_data = UsuarioConsulado.objects.filter(usuario=self.request.user)[0]
            self.initial['tomo'] = pre_data.tomo
            self.initial['consulado_list'] = '%s-%s-%s' % (pre_data.consulado, pre_data.continente.id, pre_data.continente.nombre)
        return super(CuestionarioView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        response = HttpResponse(json.dumps(self.save()), content_type="application/json")
        return response

    # def get_context_data(self, **kwargs):
    #     ctx = super(CuestionarioView, self).get_context_data(**kwargs)
    #     if UsuarioConsulado.objects.filter(usuario=self.request.user).exists():
    #         ctx['pre_data'] = UsuarioConsulado.objects.filter(usuario=self.request.user)[0]
    #     return ctx

    def save(self):
        _consulado = self.request.POST.get('consulado_list')
        _pais = self.request.POST.get('pais_list')
        cuestionario = None
        if _consulado:
            _consulado = _consulado.split('-')
            _pais = _pais.split('-')
            try:
                consulado = Consulado.objects.get(id=_consulado[0], continente=_consulado[1])
                pais = Pais.objects.get(id=_pais[0])
                continentePais = pais.continente
                continenteConsulado = consulado.continente
            except Exception:
                consulado = Consulado()
                continentePais = Continente()
                continenteConsulado = Continente()
                pais = Pais()
            cuestionario = Cuestionario(usuario=self.request.user, consulado=consulado, continentePais=continentePais,
                                        continenteConsulado=continenteConsulado, pais=pais)
        form = CuestionarioForm(self.request.POST, instance=cuestionario)
        if form.is_valid():
            form.save()
            response = {
                'success': True,
                'error': None,
                'data': 'Todo bien'
            }
        else:
            response = {
                'success': False,
                'error': True,
                'data': form.errors
            }
        return response


class AdminView(TemplateView):
    template_name = 'cuestionario/admin.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AdminView, self).dispatch(*args, **kwargs)


class TotalDigitacionListView(ListView):
    model = TotalDigitacion
    template_name = 'cuestionario/total-digitacion.html'
    paginate_by = 10

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TotalDigitacionListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        qs = super(TotalDigitacionListView, self).get_queryset()
        filtro = {}
        qs = qs.filter(**filtro)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super(TotalDigitacionListView, self).get_context_data()
        form = TotalDigitacionForm(self.request.GET)
        ctx['form'] = form
        return ctx


class ResumenDigitacionListView(ListView):
    model = ResumenDigitacion
    template_name = 'cuestionario/resumen-digitacion.html'
    paginate_by = 10

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ResumenDigitacionListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        qs = super(ResumenDigitacionListView, self).get_queryset()
        filtro = {}
        qs = qs.filter(**filtro)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super(ResumenDigitacionListView, self).get_context_data()
        form = ResumenDigitacionForm(self.request.GET)
        ctx['form'] = form
        return ctx