from django import template

register = template.Library()


@register.filter
def filter_by_buddy(value, buddy):
    return value.filter(buddy=buddy)[0]
