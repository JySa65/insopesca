from django.db import models
from utils.Select import Selects
from django.utils.translation import ugettext, ugettext_lazy as _
from authentication.models import User
from django.utils import timezone
import datetime
# Create your models here.

class Species(models.Model):
    ordinary_name = models.CharField(_("Nombre Ordinario"),max_length=50,null=False,blank=False)
    scientific_name = models.CharField(_("Nombre Cientifico"),max_length=50,null=False,blank=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (self.ordinary_name)


class Production_unit(models.Model):
    type_document = models.CharField(_("Tipo de Documento"),max_length=50, blank=False,null=False,choices= Selects().type_document())
    document = models.CharField(_("Documento"),max_length=10, blank=False,null=False)
    name = models.CharField(_("Nombre"),max_length=50, blank=False,null=False)
    landline = models.CharField(_("Telefono Fijo"),max_length=11, blank=False,null=False)
    municipality =  models.CharField(_("Municipio"),max_length=50, blank=False,null=False)
    state =  models.CharField(_("Estado"),max_length=50, blank=False,null=False)
    parish =  models.CharField(_("Parroquia"),max_length=11, blank=False,null=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return (self.name)


class Repre_unit_productive(models.Model):
    production_unit = models.OneToOneField(Production_unit, on_delete=models.CASCADE)
    type_document_repre = models.CharField(_("Tipo de Documento"),max_length=50, blank=False,null=False,choices= Selects().type_document())
    document_repre = models.CharField(_("Documento"),max_length=10, blank=False,null=False)
    name_repre = models.CharField(_("Nombre"),max_length=50, blank=False,null=False)
    last_name_repre = models.CharField(_("Apellido"),max_length=50,blank=True,null=True)
    landline_repre = models.CharField(_("Telefono Fijo"),max_length=11, blank=False,null=False)
    phone_repre = models.CharField(_("Telefono Movil"),max_length=11,blank=False,null=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pk)

class Cardinal_points(models.Model):
    production_unit = models.OneToOneField(Production_unit, on_delete=models.CASCADE)
    north  = models.IntegerField(_("Norte"))
    south = models.IntegerField(_("Sur"))
    west = models.IntegerField(_("Este"))
    oest = models.IntegerField(_("Oeste"))
    altitude = models.IntegerField(_("Altitud"))
    total_area_terr = models.IntegerField(_("Area total del Terreno"),null=False,blank=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.production_unit.name)


class Lagoon(models.Model):
    producion_unit = models.ForeignKey(Production_unit,on_delete= models.CASCADE)
    lagoon_diameter = models.IntegerField(_("Diametro de la Laguna"),blank=False,null=False)
    lagoon_deepth = models.IntegerField(_("Profundidad de la Laguna "),blank=False,null=False)
    total_area_mirror_guater = models.IntegerField(_("Area total de Terreno"),blank=False,null=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pk)


class Well(models.Model):
    producion_unit = models.ForeignKey(Production_unit,on_delete= models.CASCADE)
    well_diameter = models.IntegerField(_("Diametro del Pozo"),blank=False,null=False)
    well_deepth = models.IntegerField(_("Profundidad del Pozo"),blank=False,null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pk)


class Tracing(models.Model):
    producion_unit = models.ForeignKey(Production_unit,on_delete= models.CASCADE)
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


class Well_tracing(models.Model):
    tracing = models.ForeignKey(Tracing,on_delete= models.CASCADE)
    well = models.ForeignKey(Well,on_delete= models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.tracing)


class Lagoon_tracing(models.Model):
    tracing = models.ForeignKey(Tracing,on_delete= models.CASCADE)
    lagoon = models.ForeignKey(Lagoon,on_delete= models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.tracing)
