from django import template


register = template.Library()


@register.filter(name="check_writer")
def check_writer(user, group_name):
    return user.groups.filter(name=group_name).exists() and user.usermodel.is_writer