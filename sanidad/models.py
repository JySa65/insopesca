from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from core import models as core
import uuid
# Create your models here.


class Account(core.Account):
    def __str__(self):
        return self.document


class Company(core.Company):
    cod_permission = models.CharField(_('Codigo del Permiso'), max_length=30)
    cod_register_mercantil = models.CharField(
        _('Codigo de Registro Mercantil'), max_length=30)
    account = models.ManyToManyField(Account, verbose_name=_('Personas'))

    def __str__(self):
        return self.document

    def get_transports_all(self):
        return self.transport_set.all()

    def get_transports_all_land(self):
        return self.transport_set.all().filter(type='land')

    def get_transports_all_maritime(self):
        return self.transport_set.all().filter(type='maritime')

    def get_accounts(self):
        return self.account.all().order_by('-created_at')


class Transport(models.Model):
    company = models.ManyToManyField(Company, verbose_name=_('Empresas'))

    id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    type = models.CharField(_('Tipo'), max_length=20)

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

# CompanyInspection
# FishInspection
# CannedInspection
# VehicleInspection
