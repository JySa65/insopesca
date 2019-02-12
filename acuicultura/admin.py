from django.contrib import admin
from acuicultura.models import ProductionUnit, Specie, CardinalPoint,RepreUnitProductive,Lagoon,LagoonTracing,Well,WellTracing,Tracing
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group

# Register your models here.


# Register your models here.

admin.site.register(ProductionUnit)
admin.site.register(Specie)
admin.site.register(Lagoon)
admin.site.register(Well)
admin.site.register(LagoonTracing)
admin.site.register(WellTracing)
admin.site.register(Tracing)

class CardinaPointAdmin(admin.ModelAdmin):
    fields = ("north", "south", "west", "oest", "altitude","total_area_terr", "production_unit")

admin.site.register(CardinalPoint,CardinaPointAdmin)


class RepreUnitAdmin(admin.ModelAdmin):
    fields = ("type_document_repre","document_repre","name_repre","last_name_repre","landline_repre","phone_repre","production_unit",'is_active')

admin.site.register(RepreUnitProductive,RepreUnitAdmin)
