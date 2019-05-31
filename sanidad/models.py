from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext, ugettext_lazy as _
from django.db import models
from core import models as core
from authentication import models as authentication
import uuid
from utils.Select import Selects
from datetime import date
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
    speg = models.CharField(max_length=4, verbose_name=_('SPES'))
    type_company = models.ForeignKey(TypeCompany,
                                     on_delete=models.CASCADE,
                                     verbose_name=_('Tipo De Compañia'))
    is_inspection = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.get_document()} {self.name}"

    def get_accounts(self):
        return CompanyHasAccount.objects.filter(company__id=self.id)

    def get_transports_all(self):
        return self.transport_set.all()

    def get_transports_all_land(self):
        return Transport.objects.filter(
            company_driver_id=self.id,
            type='is_land'
        )

    def get_transports_all_maritime(self):
        return Transport.objects.filter(
            company_driver_id=self.id,
            type='is_maritime'
        )

    def get_transports_all_fluvial(self):
        return Transport.objects.filter(
            company_driver_id=self.id,
            type='is_fluvial'
        )

    def get_inspections(self, date1="", date2=""):
        inspections = Inspection.objects.filter(
            company_account_id=self.id,
            date__year=date.today().year)
        if date1 != "":
            inspections = inspections.filter(
                date__year__range=(
                    self.get_year_or_week(date1)[0], self.get_year_or_week(date2)[0]),
                date__week__range=(
                    self.get_year_or_week(date1)[1], self.get_year_or_week(date2)[1]))
        return inspections

    def get_year_or_week(self, year_week):
        return year_week.split('-')


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


class Driver(core.Account):
    is_inspection = models.BooleanField(default=False)

    def __str__(self):
        return self.document

    def get_transports_all_land(self):
        return Transport.objects.filter(
            company_driver_id=self.id,
            type='is_land'
        )

    def get_transports_all_maritime(self):
        return Transport.objects.filter(
            company_driver_id=self.id,
            type='is_maritime'
        )

    def get_transports_all_fluvial(self):
        return Transport.objects.filter(
            company_driver_id=self.id,
            type='is_fluvial'
        )

    def get_inspections(self, date1="", date2=""):
        inspections = Inspection.objects.filter(
            company_account_id=self.id)
        if date1 != "":
            inspections = inspections.filter(
                date__year__range=(
                    self.get_year_or_week(date1)[0], self.get_year_or_week(date2)[0]),
                date__week__range=(
                    self.get_year_or_week(date1)[1], self.get_year_or_week(date2)[1]))
        return inspections

    def get_year_or_week(self, year_week):
        return year_week.split('-')


class Transport(models.Model):
    company_driver_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE)
    company_driver_id = models.UUIDField()
    company_driver = GenericForeignKey(
        'company_driver_type', 'company_driver_id')

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

    # fluvial
    name_fluvial = models.CharField(
        _('Nombre'), max_length=20, null=True, blank=True)
    type_vessel = models.CharField(
        _('Tipo De Embarcación'), max_length=20,
        null=True, blank=True,
        choices=Selects().type_vissel())
    result = models.CharField(
        _('Resultado'), max_length=9999, null=True, blank=True)

    is_active = models.BooleanField(default=True, verbose_name=_('Activo'))
    is_delete = models.BooleanField(default=False, verbose_name=_('Eliminado'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.type


class PlantIce(models.Model):
    type_ice = models.CharField(max_length=20, choices=Selects().type_ice())
    state = models.ForeignKey(core.State, on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    capacity_ton = models.DecimalField(max_digits=5, decimal_places=2)
    capacity_ton_mes = models.DecimalField(max_digits=5, decimal_places=2)


class Inspection(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    company_account_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE)
    company_account_id = models.UUIDField()
    company_account = GenericForeignKey(
        'company_account_type', 'company_account_id')
    date = models.DateField(verbose_name=_('Fecha de la Inspección'))
    result = models.CharField(
        max_length=15, choices=Selects().inspection_result(),
        verbose_name=_('Resultados'))
    next_date = models.DateField(verbose_name=_(
        'Fecha de la siguiente Inspección'))
    notes = models.TextField(null=True, blank=True,
                             verbose_name=_('Observaciones'))
    pass_inspection = models.BooleanField(default=False)
    account_register = models.ForeignKey(authentication.User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return str(self.company_account)
