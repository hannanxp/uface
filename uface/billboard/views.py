# Create your views here.
from django.http import HttpResponse
from django.utils import simplejson

def index(request):
    return HttpResponse('Hello Kitty')
    
def test(request):
    data = {'a': 1, 'b': 2, 'john' : 'done', 'jane' : 'doe'}
    ret = simplejson.dumps(data)
    return HttpResponse(ret, 'application/javascript')