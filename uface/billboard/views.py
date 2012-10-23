# Create your views here.
from django.http import HttpResponse
from django.utils import simplejson
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from postman.models import Message
try:
    from django.utils.timezone import now   # Django 1.4 aware datetimes
except ImportError:
    from datetime import datetime
    now = datetime.now
from billboard.models import BbApps

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

def _delete_msg(user, msg_id):
    msg = Message.objects.get(pk=msg_id)
    message = ''
    if msg.recipient == user:
        msg.recipient_deleted_at = now()
        msg.save()
        status = True
    else:
        status = False
        message = 'User is not the message recipien'
    
    res = {'status': status, 'message': message, 'msg_id': msg_id}
    return res

def index(request):
    user = request.user
    data = {}
    ret = simplejson.dumps(data)
    return HttpResponse(ret, 'application/javascript')
    
# Change Box Position
def saveapps(request):
    user = request.user
    apps = request.POST['apps']
    
    apps_data = apps.split(',')
    for row in apps_data:
        obj = row.split(':')
        modcol = obj[0]
        modweight = obj[1]
        modname = obj[2]
        #print modcol, modweight, modname, '--------------'
        get_or_create_bbapp(user, modcol, modweight, modname)
    
    data = {}
    ret = simplejson.dumps(data)
    
    return HttpResponse(ret, 'application/javascript')
    
# Mark message to archived by reader
def acceptmsg(request):
    user = request.user
    msg_id = request.POST['msg_id']
    result = _archive_msg(user, msg_id)
    
    data = result
    ret = simplejson.dumps(data)
    return HttpResponse(ret, 'application/javascript')

# Delete message by recipient
def delmsg(request):
    user = request.user
    msg_id = request.POST['msg_id']
    result = _delete_msg(user, msg_id)
    
    data = result
    ret = simplejson.dumps(data)
    return HttpResponse(ret, 'application/javascript')

def get_or_create_bbapp(user, modcol, modweight, modname):
    try:
        box = BbApps.objects.get(user=user, modname=modname)
        box.modcol = modcol
        box.modweight = modweight
        box.save()
    except ObjectDoesNotExist:
        box = BbApps(user=user, modcol=modcol, modweight=modweight, modname=modname)
        box.save()
    return box
