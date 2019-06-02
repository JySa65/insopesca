from django.contrib import admin
from acuicultura.models import ProductionUnit, Specie, CardinalPoint,RepreUnitProductive,Lagoon,LagoonTracing,Well,WellTracing,Tracing,LagoonEspecies, \
    InspectionLagoon, RepreUnitProductiveMany, StatusInsopesca
# from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group

# Register your models here.


# Register your models here.

admin.site.register(StatusInsopesca)
admin.site.register(ProductionUnit)
admin.site.register(Specie)
admin.site.register(Lagoon)
admin.site.register(Well)
admin.site.register(LagoonTracing)
admin.site.register(WellTracing)
admin.site.register(Tracing)
admin.site.register(LagoonEspecies)
admin.site.register(InspectionLagoon)
admin.site.register(RepreUnitProductiveMany)


class CardinaPointAdmin(admin.ModelAdmin):
    fields = ("north", "south", "west", "oest", 
    "altitude","total_area_terr", "production_unit")

admin.site.register(CardinalPoint,CardinaPointAdmin)


class RepreUnitAdmin(admin.ModelAdmin):
    fields = ("type_document","document",
        "name","last_name","tlf","tlf_house",
        "production_unit",'is_active')

admin.site.register(RepreUnitProductive,RepreUnitAdmin)
