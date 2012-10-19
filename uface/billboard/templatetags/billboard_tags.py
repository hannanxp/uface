"""
Produce re-ordering module apps at admin index page

Usage:

    {% billboard_apps app_list as new_app_list %}

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
        
        new_obj_list = []
        # do reorder obj_list here...
        # Todo: cari current user
        user = User.objects.get(pk=1)
        
        # initial data population
        for app in obj_list:
            modname = app['name']
            
            try:
                bbapp = BbApps.objects.get(user=user, modname=modname)
                
            except ObjectDoesNotExist:
                bbapp = BbApps(user=user, modname=modname, modcol=0, modweight=0)
                bbapp.save()
            
            new_app = app
            new_app['modcol'] = bbapp.modcol
            new_app['modweight'] = bbapp.modweight
                
            new_obj_list.append(new_app)
            
        # sort app list
        
    
            
        context[self.var_name] = new_obj_list
        return ''

@register.tag
def billboard_apps(parser, token):
    """Converts app_list into custom order list"""
    try:
        tag_name, target_name, the_as, var_name, var_name1, var_name2 = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires exactly five arguments" % token.contents.split()[0])
        
    if the_as != 'as':
        raise template.TemplateSyntaxError("second argument to 'billboard_apps' tag must be 'as'")

    target = parser.compile_filter(target_name)
    
    return BillboarAppNode(target, var_name)