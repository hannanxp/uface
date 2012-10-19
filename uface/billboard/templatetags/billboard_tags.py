"""
Produce re-ordering module apps at admin index page

Usage:

    {% billboard_apps app_list as new_app_list %}

"""

from django import template

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
        
        # do reorder obj_list here...
        
        context[self.var_name] = obj_list
        return ''

@register.tag
def billboard_apps(parser, token):
    """Converts app_list into custom order list"""
    try:
        tag_name, target_name, the_as, var_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires exactly three arguments" % token.contents.split()[0])
        
    if the_as != 'as':
        raise template.TemplateSyntaxError("second argument to 'billboard_apps' tag must be 'as'")

    target = parser.compile_filter(target_name)
    
    return BillboarAppNode(target, var_name)