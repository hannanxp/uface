# Create your views here.
from django.http import HttpResponse
from django.utils import simplejson
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from billboard.models import BillboardUserModuleBox
from postman.models import Message

def _get_messages(user):
    msgs_i = []
    msgs_p = []
    msgs_u = []
    messages = Message.objects.filter(recipient=user)
    for msg in messages:
        if msg.category == 'i':
            msgs_i.append({'id': msg.id,'s': msg.subject,'b': msg.body,'a': msg.recipient_archived})
        elif msg.category == 'p':
            msgs_p.append({'id': msg.id,'s': msg.subject,'b': msg.body,'a': msg.recipient_archived})
        elif msg.category == 'u':
            msgs_u.append({'id': msg.id,'s': msg.subject,'b': msg.body,'a': msg.recipient_archived})

    data = {'i': msgs_i, 'p': msgs_p, 'u': msgs_u}
    return data

def _archive_msg(user, msg_id):
    msg = Message.objects.get(pk=msg_id)
    message = ''
    if msg.recipient == user:
        msg.recipient_archived = 1
        msg.save()
        status = True
    else:
        status = False
        message = 'User is not the message recipien'
    
    res = {'status': status, 'message': message, 'msg_id': msg_id}
    return res

def index(request):
    user = user_from_session_key(request.session.session_key)
    data = _get_messages(user)
    ret = simplejson.dumps(data)
    return HttpResponse(ret, 'application/javascript')
    
def test(request):
    data = {'a': 1, 'b': 2, 'john' : 'done', 'jane' : 'doe'}
    ret = simplejson.dumps(data)
    return HttpResponse(ret, 'application/javascript')
    
# Initial ajax request
def load(request):
    
    user = user_from_session_key(request.session.session_key)
    jsbox = []
    boxes = BillboardUserModuleBox.objects.filter(user=user)
    for box in boxes:
        jsbox.append({'modname': box.modname, 'posx': box.posx, 'posy': box.posy})

    messages = _get_messages(user);
    data = {'jsbox': jsbox, 'messages': messages}
    ret = simplejson.dumps(data)
    
    return HttpResponse(ret, 'application/javascript')
    
# Change Box Position
def chpos(request):
    user = user_from_session_key(request.session.session_key)
    
    box = get_or_create_userbox(user, request.POST['modname'])
    box.posx = request.POST['posx']
    box.posy = request.POST['posy']
    box.save()
    data = {}
    ret = simplejson.dumps(data)
    
    return HttpResponse(ret, 'application/javascript')
    
# Change Box Position
def saveapps(request):
    user = user_from_session_key(request.session.session_key)
    apps = request.POST['apps']
    
    
    data = {}
    ret = simplejson.dumps(data)
    
    return HttpResponse(ret, 'application/javascript')
    

    
# Mark message to archived by reader
def acceptmsg(request):
    user = user_from_session_key(request.session.session_key)
    
    result = _archive_msg(user, request.POST['msg_id'])
    
    data = result
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