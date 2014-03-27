from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import FormView, TemplateView
from django.http.response import HttpResponseRedirect, HttpResponse, Http404
from django.views.generic.base import RedirectView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
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

    def save(self):
        _consulado = self.request.POST.get('consulado_list')
        _pais = self.request.POST.get('pais_list')
        cuestionario = Cuestionario(usuario=self.request.user)
        if _consulado:
            _consulado = _consulado.split('-')
            cuestionario.consulado = _consulado[0]
            cuestionario.continenteConsulado = _consulado[1]
        if _pais:
            _pais.split('-')
            cuestionario.pais = _pais[0]
            cuestionario.continentePais =  continentePais=_pais[1]
        form = CuestionarioForm(self.request.POST, instance=cuestionario)

        if form.is_valid():
            response = {
                'success': True,
                'error': None,
                'data': 'Todo bien'
            }
            try:
                form.save()
            except Exception as e:
                response['success'] = False
                response['error'] = True
                response['data'] = e.message
        else:
            response = {
                'success': False,
                'error': True,
                'data': form.errors
            }
        return response


class CuestionarioDetailView(UpdateView):
    model = Cuestionario
    template_name = 'cuestionario/cuestionario.html'
    form_class = CuestionarioForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CuestionarioDetailView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        response = HttpResponse(json.dumps(self.save()), content_type="application/json")
        return response

    def get_initial(self):
        initial = super(CuestionarioDetailView, self).get_initial()
        continente = Continente.objects.get(id=self.object.continenteConsulado)
        continente_pais = Continente.objects.get(id=self.object.continentePais)
        initial['consulado_list'] = '%s-%s-%s' % (self.object.consulado, self.object.continenteConsulado,
                                                  continente.nombre)
        initial['pais_list'] = '%s-%s-%s' % (self.object.pais, self.object.continentePais,
                                                  continente_pais.nombre)
        return initial

    def save(self):
        _consulado = self.request.POST.get('consulado_list')
        _pais = self.request.POST.get('pais_list')
        cuestionario = self.get_object()
        if _consulado:
            _consulado = _consulado.split('-')
            cuestionario.consulado = _consulado[0]
            cuestionario.continenteConsulado = _consulado[1]
        if _pais:
            _pais = _pais.split('-')
            cuestionario.pais = _pais[0]
            cuestionario.continentePais = _pais[1]
        form = CuestionarioForm(self.request.POST, instance=cuestionario)
        if form.is_valid():
            response = {
                'success': True,
                'error': None,
                'data': 'Todo bien'
            }
            try:
                form.save()
            except Exception as e:
                response['success'] = False
                response['error'] = True
                response['data'] = e.message
        else:
            response = {
                'success': False,
                'error': True,
                'data': form.errors
            }
        return response


class CuestionarioAjaxView(TemplateView):
    def dispatch(self, request, *args, **kwargs):
        if not request.is_ajax():
            raise Http404("Only ajax.")
        return super(CuestionarioAjaxView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        tomo = request.POST['tomo']
        ficha = request.POST['ficha']
        _consulado = request.POST.get('consulado_list')
        if _consulado == '' or _consulado is None:
            _consulado = "-"
        _consulado = _consulado.split('-')
        cuestionario = Cuestionario.objects.filter(tomo=tomo, ficha=ficha, consulado=_consulado[0],
                                                   continenteConsulado=_consulado[1])
        pk = None
        if cuestionario.exists():
            pk = cuestionario.values_list('id')[0]

        if pk is None:
            data = {
                'success': False,
                'error': True,
                'data': 'No existe la ficha buscada'
            }
        else:
            data = {
                'success': True,
                'error': False,
                'data': pk
            }
        response = HttpResponse(json.dumps(data), content_type="application/json")
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
        if not self.request.user.is_superuser:
            return HttpResponseRedirect('/cuestionario/')
        return super(TotalDigitacionListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        qs = super(TotalDigitacionListView, self).get_queryset()
        filtro = {}
        if self.request.GET.get('date_range'):
            date_range = self.request.GET['date_range'].split(' | ')
            filtro['fecha__range'] = date_range
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
    paginate_by = 2

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_superuser:
            return HttpResponseRedirect('/cuestionario/')
        return super(ResumenDigitacionListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        qs = super(ResumenDigitacionListView, self).get_queryset()
        filtro = {}
        if self.request.GET.get('date_range'):
            date_range = self.request.GET['date_range'].split(' | ')
            filtro['fecha__range'] = date_range
        if 'digitador' in self.request.GET:
            filtro['digitador'] = self.request.GET['digitador']
        qs = qs.filter(**filtro)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super(ResumenDigitacionListView, self).get_context_data()
        form = ResumenDigitacionForm(self.request.GET)
        ctx['form'] = form
        return ctx