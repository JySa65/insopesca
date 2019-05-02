from django.db import models
from utils.Select import Selects
from decimal import Decimal
from django.core.validators import MinValueValidator
from django.utils.translation import ugettext, ugettext_lazy as _
from authentication.models import User
from django.utils import timezone
import datetime
from core import models as core
import uuid
# Create your models here.


class Specie(models.Model):
    """
    Se Registra las especies
    """

    ordinary_name = models.CharField(
        _("Nombre Ordinario"), max_length=50, null=True, blank=True)
    scientific_name = models.CharField(
        _("Nombre Cientifico"), max_length=50, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.ordinary_name} - {self.scientific_name}"


class ProductionUnit(core.Company):
    """
    Esta Clase hereda de company hace una relacion OneToOne
    """

    def __str__(self):
        return f"{self.get_document()} {self.get_full_name()}"


class RepreUnitProductive(core.Account):
    """
    Esta clase es para el representante de la unidad productora
    """
    # id = models.UUIDField(
    # default=uuid.uuid4, editable=False, unique=True, primary_key=True)

    production_unit = models.ForeignKey(
        ProductionUnit, on_delete=models.CASCADE)
    # type_document_repre = models.CharField(
    #     _("Tipo de Documento"), max_length=50, blank=False, null=False, choices=Selects().type_document())
    # document_repre = models.CharField(
    #     _("Documento"), max_length=10, blank=False, null=False, unique=True)
    # name_repre = models.CharField(
    #     _("Nombre"), max_length=50, blank=False, null=False)
    # last_name_repre = models.CharField(
    #     _("Apellido"), max_length=50, blank=True, null=True)
    # landline_repre = models.CharField(
    #     _("Telefono Casa"), max_length=11, blank=False, null=False)
    # phone_repre = models.CharField(
    #     _("Telefono Movil"), max_length=11, blank=False, null=False)
    # is_active = models.BooleanField(_('Es Activo'), default=True)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_full_name()}"


class CardinalPoint(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True)

    production_unit = models.OneToOneField(
        ProductionUnit, on_delete=models.CASCADE)

    north = models.FloatField(_("Norte"), null=False, blank=False)

    south = models.FloatField(_("Sur"), null=False, blank=False)

    west = models.FloatField(_("Este"), null=False, blank=False)

    oest = models.FloatField(_("Oeste"), null=False, blank=False)

    altitude = models.FloatField(_("Altitud"), null=False, blank=False)

    total_area_terr = models.FloatField(
        _("Area total del Terreno"), null=False, blank=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.production_unit.get_full_name()


class Lagoon(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True)

    producion_unit = models.ForeignKey(
        ProductionUnit, on_delete=models.CASCADE)

    lagoon_diameter = models.FloatField(
        _("Ancho de la Laguna"), blank=False, null=False)

    lagoon_deepth = models.FloatField(
        _("Largo de la Laguna "), blank=False, null=False)

    total_area_mirror_guater = models.FloatField(
        _("Area total de Terreno"), blank=True, null=True)

    sistem_cultivate = models.CharField(
        _("Sistema de Cultivo"), max_length=50, blank=True, null=True, choices=Selects().type_cultive())

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pk)


class Well(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    producion_unit = models.ForeignKey(
        ProductionUnit, on_delete=models.CASCADE)
    well_diameter = models.FloatField(
        _("Diametro del Pozo"), blank=False, null=False)

    well_deepth = models.FloatField(
        _("Profundidad del Pozo"), blank=False, null=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pk)


class Tracing(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True)

    producion_unit = models.ForeignKey(
        ProductionUnit, on_delete=models.CASCADE)
    number_lagoon = models.PositiveIntegerField(
        _("Numero de Lagunas"), null=False, blank=False)
    new_number_lagoon = models.PositiveIntegerField(
        _("Numero de Nuevas de Lagunas"), null=False, blank=False)
    number_well = models.PositiveIntegerField(
        _("Numero de Pozos"), null=False, blank=False)
    new_number_well = models.PositiveIntegerField(
        _("Numero de  Nuevos Pozos "), null=False, blank=False)

    illegal_superfaces = models.PositiveIntegerField(
        _("Numero de Superficies Ilegales"), blank=False, null=False)
    irregular_superfaces = models.PositiveIntegerField(
        _("Numero de Superficies Irregulares"), blank=False, null=False)
    permise_superfaces = models.PositiveIntegerField(
        _("Numero de Superficies Permisadas"), blank=False, null=False)
    regular_superfaces = models.PositiveIntegerField(
        _("Numero de Superficies regulares"), blank=False, null=False)
    responsible = models.ForeignKey(User, on_delete=models.CASCADE)

    date = models.DateField(verbose_name=_('Fecha Del Seguimiento'),
                            blank=True, null=True)
    date_next = models.DateField(verbose_name=_('Fecha Del Siguiente Seguimiento'),
                                 blank=True, null=True)

    notes = models.TextField(null=True, blank=True,
                             verbose_name=_('Observaciones'))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pk)


class WellTracing(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True)

    tracing = models.ForeignKey(Tracing, on_delete=models.CASCADE)
    well = models.ForeignKey(Well, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.tracing)


class LagoonTracing(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True)

    tracing = models.ForeignKey(Tracing, on_delete=models.CASCADE)
    lagoon = models.ForeignKey(Lagoon, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.tracing)


class LagoonEspecies(models.Model):
    lagoon = models.ForeignKey(Lagoon, on_delete=models.CASCADE)
    especies = models.ForeignKey(Specie, on_delete=models.CASCADE)
    number_specie = models.IntegerField()

    def __str__(self):
        return str(self.especies)
