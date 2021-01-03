'''
# View your settings and config on the production system.

urlpatterns = [
    ....
    re_path(r'^config', config_view.config, name='config'),
]
'''

from django.conf import settings
from django.http import HttpResponseForbidden, HttpResponse
from django.template import Template, Context


def config(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()

    all_settings = []
    for key in dir(settings):
        if key.startswith('_'):
            continue
        all_settings.append((key, getattr(settings, key)))
    return HttpResponse(Template('''
    <h1>request</h1>
    <table>
     <tr><td>request.get_host()</td><td>{{ request.get_host }}</td></tr>
     <tr><td>request.build_absolute_uri()</td><td>{{ request.build_absolute_uri }}</td></tr>
    </table>
     
    <h1>request.META</h1>
    <table>
     {% for key, value in request.META.items %}
       <tr><td>{{ key }}</td><td>{{ value }}</td></tr>
      {% endfor %} 
    </table>
    
    <h1>settings</h1>
    <table>
     {% for key, value in all_settings %}
       <tr><td>{{ key }}</td><td>{{ value }}</td></tr>
      {% endfor %} 
    </table>
         
    ''').render(Context(dict_=dict(request=request, all_settings=all_settings))))
