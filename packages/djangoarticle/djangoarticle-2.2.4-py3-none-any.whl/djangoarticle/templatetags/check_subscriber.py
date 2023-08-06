from django import template


register = template.Library()


@register.filter(name="check_subscriber")
def check_subscriber(user, group_name):
    return user.groups.filter(name=group_name).exists()