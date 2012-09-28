# Create your views here.
from django.http import HttpResponse
from django.utils import simplejson
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from billboard.models import BillboardUserModuleBox

def index(request):
    return HttpResponse('Hello Kitty')
    
def test(request):
    data = {'a': 1, 'b': 2, 'john' : 'done', 'jane' : 'doe'}
    ret = simplejson.dumps(data)
    return HttpResponse(ret, 'application/javascript')
    
# Initial ajax request
def load(request):
    
    user = user_from_session_key(request.session.session_key)
    data = {'id': user.id, 'username': user.username}
    ret = simplejson.dumps(data)
    
    return HttpResponse(ret, 'application/javascript')
    
# Change Box Position
def chpos(request):
    user = user_from_session_key(request.session.session_key)
    modname = request.POST['modname']
    box = get_or_create_userbox(user, modname)
    data = {}
    ret = simplejson.dumps(data)
    
    return HttpResponse(ret, 'application/javascript')
    
def user_from_session_key(session_key):
    from django.conf import settings
    from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY, load_backend
    from django.contrib.auth.models import AnonymousUser

    session_engine = __import__(settings.SESSION_ENGINE, {}, {}, [''])
    session_wrapper = session_engine.SessionStore(session_key)
    session = session_wrapper.load()
    user_id = session.get(SESSION_KEY)
    backend_id = session.get(BACKEND_SESSION_KEY)
    if user_id and backend_id:
        auth_backend = load_backend(backend_id)
        user = auth_backend.get_user(user_id)
        if user:
            return user
    return AnonymousUser()
    
def get_or_create_userbox(user, modname):
    try:
        box = BillboardUserModuleBox.objects.get(user=user, modname=modname)
    except ObjectDoesNotExist:
        box = BillboardUserModuleBox(user=user, modname=modname, posx=-1, posy=-1)
        box.save()
    return box