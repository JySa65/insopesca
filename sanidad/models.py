from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from core import models as core
from utils.Select import Selects
import uuid
# Create your models here.


class Account(core.Account):
    def __str__(self):
        return self.document


class TypeCompany(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super().save(*args, **kwargs)


class Company(core.Company):
    speg = models.CharField(max_length=4, verbose_name=_('SPEG'))
    type_company = models.ForeignKey(TypeCompany, 
            on_delete=models.CASCADE, verbose_name=_('Tipo De Compañia'))

    def __str__(self):
        return self.document

    def get_accounts(self):
        return CompanyHasAccount.objects.filter(company__id=self.id)

    def get_transports_all(self):
        return self.transport_set.all()

    def get_transports_all_land(self):
        return self.transport_set.all().filter(type='is_land')

    def get_transports_all_maritime(self):
        return self.transport_set.all().filter(type='is_maritime')



class CompanyHasAccount(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    account_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company.name



class Transport(models.Model):
    company = models.ManyToManyField(Company, verbose_name=_('Empresas'))

    id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    type = models.CharField(_('Tipo'), max_length=20,
                            choices=Selects().type_transport())

    # land
    registration = models.CharField(
        _('Matricula'), max_length=20, null=True, blank=True)
    model = models.CharField(_('Modelo'), max_length=20, null=True, blank=True)
    brand = models.CharField(_('Marca'), max_length=20, null=True, blank=True)
    load_capacity = models.CharField(
        _('Capacidad de Carga'), max_length=20, null=True, blank=True)

    # maritime
    name = models.CharField(_('Nombre'), max_length=20, null=True, blank=True)
    year_vessel = models.CharField(
        _('Año De Embarcación'), max_length=20, null=True, blank=True)

    is_active = models.BooleanField(default=True, verbose_name=_('Activo'))
    is_delete = models.BooleanField(default=False, verbose_name=_('Eliminado'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.type


class Driver(core.Account):
    transport = models.ManyToManyField(Transport, verbose_name="Conductor")

    def __str__(self):
        return self.document
