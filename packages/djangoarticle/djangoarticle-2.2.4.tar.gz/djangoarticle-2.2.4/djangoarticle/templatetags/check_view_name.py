from django import template


register = template.Library()


@register.filter(name="check_view_name")
def check_view_name(view_name, static_view_name):
    return view_name == static_view_name