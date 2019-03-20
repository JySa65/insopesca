from django.contrib import admin
from core.models import State, Municipality, Parish, Notification
# Register your models here.

admin.site.register(State)
admin.site.register(Municipality)
admin.site.register(Parish)
admin.site.register(Notification)
