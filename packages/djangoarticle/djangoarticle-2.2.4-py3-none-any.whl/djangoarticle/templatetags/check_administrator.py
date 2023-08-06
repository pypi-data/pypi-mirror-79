from django import template


register = template.Library()


@register.filter(name="check_administrator")
def check_administrator(user, group_name):
     return user.groups.filter(name=group_name) and user.usermodel.is_administrator