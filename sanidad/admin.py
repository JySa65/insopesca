from django.contrib import admin
from sanidad.models import Account, Company, Driver, Transport
# Register your models here.

admin.site.register(Account)
admin.site.register(Company)
admin.site.register(Driver)
admin.site.register(Transport)

# date_hierarchy
