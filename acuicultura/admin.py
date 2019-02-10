from django.contrib import admin
from acuicultura.models import Production_unit, Species, Cardinal_point,Repre_unit_productive
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group

# Register your models here.


class Production__unit_view_admin(admin.ModelAdmin):
    fields = ('type_document', 'document', 'name', 'landline',
              'phone', 'operative', 'municipality', 'state', 'parish','is_delete')
    ordering_by = ('-id')


admin.site.register(Production_unit, Production__unit_view_admin)


class CardinaPointAdmin(admin.ModelAdmin):
    fields = ("north", "south", "west", "oest", "altitude","total_area_terr", "production_unit")

admin.site.register(Cardinal_point,CardinaPointAdmin)


class RepreUnitAdmin(admin.ModelAdmin):
    fields = ("type_document_repre","document_repre","name_repre","last_name_repre","landline_repre","phone_repre","production_unit")

admin.site.register(Repre_unit_productive,RepreUnitAdmin)
