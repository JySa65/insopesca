from django.contrib import admin
from django.conf import settings
from sanidad.models import Account, Company, Driver, Transport, \
    CompanyHasAccount, TypeCompany
# Register your models here.

admin.site.register(Account)
admin.site.register(Company)
admin.site.register(Driver)
admin.site.register(Transport)

if settings.DEBUG:
    admin.site.register(CompanyHasAccount)
    admin.site.register(TypeCompany)
# date_hierarchy
