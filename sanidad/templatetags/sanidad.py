from django import template
from core.models import Notification
from django.utils import timezone
from datetime import timedelta
register = template.Library()


@register.simple_tag()
def filter_inspection():
    date = timezone.now()
    start = date - timedelta(days=15)
    end = date + timedelta(days=15)
    data = Notification.objects.filter(
        created_at__range=(start, end), is_active=True)
    return data
