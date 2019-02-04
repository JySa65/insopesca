from django.contrib import admin
from acuicultura.models import Production_unit,Species
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group

# Register your models here.


class Production__unit_view_admin(admin.ModelAdmin):
    fields = ('type_document','document','name','landline','phone','operative','municipality','state','parish')
    ordering_by = ('-id')
admin.site.register(Production_unit,Production__unit_view_admin)


