from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from utils.Select import Selects
from datetime import datetime
import uuid
# Create your models here.


class State(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    name = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Municipality(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    name = models.CharField(max_length=1000)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Parish(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    name = models.CharField(max_length=1000)
    municipality = models.ForeignKey(
        Municipality, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Account(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    type_document = models.CharField(
        _('Tipo De Documento'), max_length=2, null=False, blank=False)
    document = models.CharField(
        _('Documento'), max_length=15, null=False, blank=False, unique=True)
    name = models.CharField(_('Nombres'), max_length=50,
                            null=False, blank=False)
    last_name = models.CharField(
        _('Apellidos'), max_length=50, null=False, blank=False)
    sex = models.CharField(_('Sexo'), max_length=15, choices=Selects().sex())
    tlf = models.CharField(_('Telefono'), max_length=15, null=True, blank=True)
    tlf_house = models.CharField(
        _('Telefono Casa'), max_length=15, null=True, blank=True)
    birthday = models.DateField(
        null=True, blank=True, verbose_name=_('Fecha de Nacimiento'))
    address = models.TextField(_('Dirección'), null=False, blank=False)
    is_active = models.BooleanField(default=True, verbose_name=_('Activo'))
    is_delete = models.BooleanField(default=False, verbose_name=_('Elimanido'))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ('-created_at',)

    def __str__(self):
        return self.name

    def get_document(self):
        return f'{self.type_document}-{self.document}'

    def get_full_name(self):
        return f'{self.name} {self.last_name}'

    def get_short_name(self):
        return self.name

    def age(self):
        return int((datetime.now().date() - self.birthday).days / 365.25)


class Company(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    type_document = models.CharField(
        _('Tipo De Documento'), max_length=2, null=False, blank=False,choices= Selects().type_document())
    document = models.CharField(
        _('Documento'), max_length=15, null=False, blank=False, unique=True)
    name = models.CharField(_('Nombres'), max_length=50,
                            null=False, blank=False)
    tlf = models.CharField(_('Telefono'), max_length=15, null=True, blank=True)
    tlf_house = models.CharField(
        _('Telefono Casa'), max_length=15, null=True, blank=True)
    state = models.ForeignKey(
        State, on_delete=models.CASCADE, verbose_name=_('Estado'))
    municipality = models.ForeignKey(
        Municipality, on_delete=models.CASCADE, verbose_name=_('Municipio'))
    parish = models.ForeignKey(
        Parish, on_delete=models.CASCADE, verbose_name=_('Parroquia'),)
    address = models.TextField(_('Direccion'), null=False, blank=False)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ('-created_at',)

    def __str__(self):
        return self.name

    def get_document(self):
        return f'{self.type_document}-{self.document}'
