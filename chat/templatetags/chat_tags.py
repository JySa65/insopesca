from django import template
from django.utils import timezone
from datetime import timedelta
register = template.Library()


@register.filter
def two_letter(value):
    name = value.name
    last_name = value.last_name
    if not name and not last_name:
        return f"{value.email[:2]}".upper()
    return f"{name[:1]}{last_name[:1]}".upper()
