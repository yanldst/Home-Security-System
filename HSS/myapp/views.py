from django.shortcuts import render
from myapp.models import Mode
from rest_framework import viewsets
from django.template import RequestContext
from myapp.serializers import ModeSerializer
import requests
import json

# Create your views here.
class ModeViewSet(viewsets.ModelViewSet):
    queryset = Mode.objects.all()
    serializer_class = ModeSerializer

def home(request):
    out = ''
    currentmode = 'photos'

    if 'photos' in request.POST:
        values = {"name": "photos"}
        r = requests.put('http://127.0.0.1:8000/mode/1/',
                        data=values, auth=('pi', 'raspberry'))
        result = r.text
        output = json.loads(result)
        out = output['name']

    if 'stream' in request.POST:
        values = {"name": "stream"}
        r = requests.put('http://127.0.0.1:8000/mode/1/',
                        data=values, auth=('pi', 'raspberry'))
        result = r.text
        output = json.loads(result)
        out = output['name']

    r = requests.get('http://127.0.0.1:8000/mode/1/',
                    auth=('pi', 'raspberry'))
    result = r.text
    output = json.loads(result)
    currentmode = output['name']

    return render(request, 'myapp/index.html', {'name':out,
    'currentmode':currentmode})
 
