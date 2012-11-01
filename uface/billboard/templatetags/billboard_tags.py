"""
Produce Billboard Message items and
re-ordering module apps at admin index page
"""

from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from billboard.models import BbApps
from postman.models import *

register = template.Library()

class BillboarAppNode(template.Node):
    def __init__(self, target, var_name):
        self.target = target
        self.var_name = var_name

    def render(self, context):
        obj_list = self.target.resolve(context, True)
        if obj_list == None:
            # target variable wasn't found in context; fail silently.
            context[self.var_name] = []
            return ''
        
        user = context['user']
        
        # initial saving
        for app in obj_list:
            modname = app['name']
            
            try:
                bbapp = BbApps.objects.get(user=user, modname=modname)
                
            except ObjectDoesNotExist:
                bbapp = BbApps(user=user, modname=modname, modcol=0, modweight=0)
                bbapp.save()
            
        # here, all app list is saved into database
        items = []
        for col in [0,1,2]:
            new_obj_list = []
            bbapps = BbApps.objects.filter(user=user, modcol=col).order_by('modweight')
            for bbapp in bbapps:
                
                # populate obj_list
                for app in obj_list:
                    if app['name'] == bbapp.modname: # obj exist
                        new_app = app
                        new_app['modcol'] = bbapp.modcol
                        new_app['modweight'] = bbapp.modweight
                        
                        new_obj_list.append(new_app)
                        
            items.append(new_obj_list)     
        
        context[self.var_name] = items
        
        return ''
    
class BillboarMessagesNode(template.Node):
    def __init__(self, var_name):
        self.var_name = var_name

    def render(self, context):
        
        user = context['user']
        bb_messages = []
        
        for catid,catname in CATEGORY_CHOICES:
            msgs = []
            #messages = Message.objects.filter(recipient=user, sender_deleted_at=None, recipient_deleted_at=None, category=catid)
            kwargs = {'category': catid}
            messages = getattr(Message.objects, 'inbox')(user, **kwargs)
            
            for msg in messages:
                
                if msg.recipient_archived:
                    classname_archived = 'archived'
                else:
                    classname_archived = ''
                    
                if msg.read_at:
                    classname_read = ''
                else:
                    classname_read = 'un-read'
                    
                mm_obj = {}
                mm_obj['id'] = msg.id
                mm_obj['subject'] = msg.subject
                mm_obj['body'] = msg.body
                mm_obj['recipient_archived'] = msg.recipient_archived
                mm_obj['classname_archived'] = classname_archived
                mm_obj['classname_read'] = classname_read
                mm_obj['category'] = msg.category
                mm_obj['obfuscated_sender'] = msg.obfuscated_sender
                mm_obj['obfuscated_recipient'] = msg.obfuscated_recipient
                mm_obj['sent_at'] = msg.sent_at
                
                msgs.append(mm_obj)
                    
            col = {}
            col['col'] = catid
            col['title'] = catname
            col['msgs'] = msgs
            bb_messages.append(col)
        
        context[self.var_name] = bb_messages
        
        return ''

@register.tag
def billboard_apps(parser, token):
    """
    Converts app_list into into several columns of app items
    Usage:
        {% billboard_apps app_list as bb_items %}
    """
    try:
        tag_name, target_name, the_as, var_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires exactly three arguments" % token.contents.split()[0])
        
    if the_as != 'as':
        raise template.TemplateSyntaxError("second argument to 'billboard_apps' tag must be 'as'")

    target = parser.compile_filter(target_name)
    
    return BillboarAppNode(target, var_name)
    
@register.tag
def billboard_messages(parser, token):
    """
    Produce Billboard Message Items
    Usage:
        {% billboard_messages as bb_messages %}
    """
    try:
        tag_name, the_as, var_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires exactly two arguments" % token.contents.split()[0])
        
    if the_as != 'as':
        raise template.TemplateSyntaxError("first argument to %r tag must be 'as'" % token.contents.split()[0])
    
    return BillboarMessagesNode(var_name)