from django import template


register = template.Library()


@register.filter(name="check_editor")
def check_editor(user, group_name):
    return user.groups.filter(name=group_name).exists() and user.usermodel.is_editor