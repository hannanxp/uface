"""
Produce Billboard Message items and
re-ordering module apps at admin index page
"""

from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from billboard.models import BbApps
from postman.models import Message

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
        msgs_i = []
        msgs_p = []
        msgs_u = []
        messages = Message.objects.filter(recipient=user, sender_deleted_at=None, recipient_deleted_at=None)
        for msg in messages:
            
            if msg.recipient_archived:
                cname = 'archived'
            else:
                cname = ''
            
            if msg.category == 'i':
                msgs_i.append({'id': msg.id,'s': msg.subject,'b': msg.body,'a': msg.recipient_archived,'c':cname,'t':msg.category})
            elif msg.category == 'p':
                msgs_p.append({'id': msg.id,'s': msg.subject,'b': msg.body,'a': msg.recipient_archived,'c':cname,'t':msg.category})
            elif msg.category == 'u':
                msgs_u.append({'id': msg.id,'s': msg.subject,'b': msg.body,'a': msg.recipient_archived,'c':cname,'t':msg.category})
    
        #data = {'i': msgs_i, 'p': msgs_p, 'u': msgs_u}
        
        col = {}
        col['col'] = 'i'
        col['title'] = 'IMPORTANT'
        col['msgs'] = msgs_i
        bb_messages.append(col)
        
        col = {}
        col['col'] = 'p'
        col['title'] = 'PERSONAL'
        col['msgs'] = msgs_p
        bb_messages.append(col)
        
        col = {}
        col['col'] = 'u'
        col['title'] = 'USEFUL'
        col['msgs'] = msgs_u
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