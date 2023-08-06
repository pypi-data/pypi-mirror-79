from django import template
from django.db.models import Q


register = template.Library()


@register.filter(name="check_admin")
def check_admin(user, group_name):
    return user.groups.filter(name=group_name).exists() and user.usermodel.is_admin