from django.http.response import HttpResponse, Http404
import json

__author__ = 'holivares'


class JSONResponseMixin(object):
    """
    A mixin that can be used to render a JSON response.
    """
    response_class = HttpResponse
    json_keys = None

    def dispatch(self, request, *args, **kwargs):
        if not request.is_ajax():
            raise Http404("Only ajax.")
        return super(JSONResponseMixin, self).dispatch(request, *args, **kwargs)

    def render_to_response(self, context, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        response_kwargs['content_type'] = 'application/json'
        return self.response_class(
            self.convert_context_to_json(context),
            **response_kwargs
        )

    def convert_context_to_json(self, context):
        """Convert the context dictionary into a JSON object"""
        data = context
        if self.json_keys:
            data = dict([(k, context[k]) for k in self.json_keys])
        return json.dumps(data)