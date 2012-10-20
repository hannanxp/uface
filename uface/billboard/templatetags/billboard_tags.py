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
    def __init__(self, target, var_name, user_id):
        self.target = target
        self.var_name = var_name
        self.user_id = user_id

    def render(self, context):
        obj_list = self.target.resolve(context, True)
        if obj_list == None:
            # target variable wasn't found in context; fail silently.
            context[self.var_name] = []
            return ''
        
        obj_user_id = self.user_id.resolve(context, True)
        user = User.objects.get(pk=obj_user_id)
        
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

@register.tag
def billboard_apps(parser, token):
    """Converts app_list into custom order list"""
    try:
        tag_name, target_name, the_as, var_name, user_id_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires exactly four arguments" % token.contents.split()[0])
        
    if the_as != 'as':
        raise template.TemplateSyntaxError("second argument to 'billboard_apps' tag must be 'as'")

    target = parser.compile_filter(target_name)
    user_id = parser.compile_filter(user_id_name)
    
    return BillboarAppNode(target, var_name, user_id)