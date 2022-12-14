from django import template

register = template.Library()


@register.filter
def admin_check(guild, buddy):
    return guild.is_admin(buddy)
