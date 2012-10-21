"""
Produce Billboard Message items and
re-ordering module apps at admin index page
"""

from django import template
from billboard.models import BbApps
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

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
        
        context[self.var_name] = user
        
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