from django.db import models
from utils.Select import Selects
from django.utils.translation import ugettext, ugettext_lazy as _
from authentication.models import User
from django.utils import timezone
import datetime
from core import models as core
import uuid
# Create your models here.

class Specie(models.Model):
    ordinary_name = models.CharField(_("Nombre Ordinario"),max_length=50,null=False,blank=False, unique=True)
    scientific_name = models.CharField(_("Nombre Cientifico"),max_length=50,null=False,blank=False, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (self.ordinary_name)

#    type_document = models.CharField(_("Tipo de Documento"),max_length=50, blank=False,null=False,choices= Selects().type_document())

class ProductionUnit(core.Company):
    def __str__(self):
        return str(self.pk)
        


class RepreUnitProductive(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True)

    production_unit = models.ForeignKey(ProductionUnit, on_delete=models.CASCADE)
    type_document_repre = models.CharField(_("Tipo de Documento"),max_length=50, blank=False,null=False,choices= Selects().type_document())
    document_repre = models.CharField(_("Documento"),max_length=10, blank=False,null=False,unique=True)
    name_repre = models.CharField(_("Nombre"),max_length=50, blank=False,null=False)
    last_name_repre = models.CharField(_("Apellido"),max_length=50,blank=True,null=True)
    landline_repre = models.CharField(_("Telefono Casa"),max_length=11, blank=False,null=False)
    phone_repre = models.CharField(_("Telefono Movil"),max_length=11,blank=False,null=False)
    is_active = models.BooleanField(_('Es Activo'), default=True)    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pk)

class CardinalPoint(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True)

    production_unit = models.OneToOneField(ProductionUnit, on_delete=models.CASCADE)
    north  = models.IntegerField(_("Norte"),null=False,blank=False)
    south = models.IntegerField(_("Sur"),null=False,blank=False)
    west = models.IntegerField(_("Este"),null=False,blank=False)
    oest = models.IntegerField(_("Oeste"),null=False,blank=False)
    altitude = models.IntegerField(_("Altitud"),null=False,blank=False)
    total_area_terr = models.IntegerField(_("Area total del Terreno"),null=False,blank=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pk)


class Lagoon(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True)

    producion_unit = models.ForeignKey(ProductionUnit,on_delete= models.CASCADE)
    lagoon_diameter = models.IntegerField(_("Diametro de la Laguna"),blank=False,null=False)
    lagoon_deepth = models.IntegerField(_("Profundidad de la Laguna "),blank=False,null=False)
    total_area_mirror_guater = models.IntegerField(_("Area total de Terreno"),blank=True,null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pk)


class Well(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    producion_unit = models.ForeignKey(ProductionUnit,on_delete= models.CASCADE)
    well_diameter = models.IntegerField(_("Diametro del Pozo"),blank=False,null=False)
    well_deepth = models.IntegerField(_("Profundidad del Pozo"),blank=False,null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pk)


class Tracing(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True)

    producion_unit = models.ForeignKey(ProductionUnit,on_delete= models.CASCADE)
    number_lagoon = models.IntegerField(_("Numero de Lagunas"),null=False,blank=False)
    new_number_lagoon = models.IntegerField(_("Numero de Nuevas de Lagunas"),null=False,blank=False)
    number_well = models.IntegerField(_("Numero de Pozos"),null=False,blank=False)
    new_number_well = models.IntegerField(_("Numero de  Nuevos Pozos "),null=False,blank=False)
    illegal_superfaces = models.IntegerField(_("Numero de Superficies Ilegales"),blank=False,null=False)
    irregular_superfaces = models.IntegerField(_("Numero de Superficies Irregulares"),blank=False,null=False)
    permise_superfaces = models.IntegerField(_("Numero de Superficies Permisadas"),blank=False,null=False)
    regular_superfaces = models.IntegerField(_("Numero de Superficies regulares"),blank=False,null=False)
    responsible = models.ForeignKey(User,on_delete= models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pk)


class WellTracing(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True)

    tracing = models.ForeignKey(Tracing,on_delete= models.CASCADE)
    well = models.ForeignKey(Well,on_delete= models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.tracing)


class LagoonTracing(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True)

    tracing = models.ForeignKey(Tracing,on_delete= models.CASCADE)
    lagoon = models.ForeignKey(Lagoon,on_delete= models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.tracing)
