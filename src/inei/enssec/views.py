from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.views.generic import FormView, TemplateView
from django.http.response import HttpResponseRedirect, HttpResponse
from inei.auth.forms import LoginForm
from django.contrib.auth import login, authenticate, logout
import json
from inei.enssec.forms import CuestionarioForm
from inei.enssec.models import Cuestionario, Consulado, Continente

__author__ = 'holivares'


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
                if user.is_admin:
                    return HttpResponseRedirect('/admin/')
                return HttpResponseRedirect(self.get_success_url())
            else:
                #cuenta deshabilitada
                return self.render_to_response(self.get_context_data(form=form))
        else:
            #login invalido
            return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse('cuestionario1')


class CuestionarioView(FormView):
    template_name = 'cuestionario/cuestionario.html'
    form_class = CuestionarioForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CuestionarioView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        response = HttpResponse(json.dumps(self.save()), content_type="application/json")
        return response

    def save(self):
        _consulado = self.request.POST.get('consulado_list')
        cuestionario = None
        if _consulado:
            _consulado = _consulado.split('-')
            try:
                consulado = Consulado.objects.get(id=_consulado[0], continente=_consulado[1])
                continente = consulado.continente
            except Consulado.DoesNotExist:
                consulado = Consulado()
                continente = Continente()
            cuestionario = Cuestionario(usuario=self.request.user, consulado=consulado, continente=continente)
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