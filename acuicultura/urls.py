from django.urls import path
from acuicultura.views import AcuiculturaHome, ProductionUnitCreateView,\
    ProductionUnitUpdate, ProductionuUnitDetail, ProductionUnitDelete, ProductionUnitList,\
    SpeciesCreateView, SpeciesList, SpeciesDetail, SpeciesUpdate, SpeciesDelete, TracingCreate, RepreUnitCreate,\
    TracingDetail, TracingUpdate, WellDetail, LagoonDetail, TracingdeleteView, Representative_unit_production_delete, Representative_unit_production_detail, \
    RepresentativeUnitProductionUpdate, TracingInspectionHomeView, \
    InspectionProductionUnitLagoon


# ,Production_unit_CreateView,Production_unit_Update,Production_unit_List, \
# Production_unit_Detail,Production_unit_Delete,SpeciesCreateView,SpeciesDelete,SpeciesDetail, \
# SpeciesList,SpeciesUpdate,TracingCreate,TracingDetail,TracingUpdate,Tracingdelete ,TracingList, \
# Representative_unit_production_create,Representative_unit_production_delete,Representative_unit_production_list,\
# Representative_unit_production_detail,Representative_unit_production_update

app_name = "acuicultura"
urlpatterns = [

    path('', AcuiculturaHome.as_view(), name="home"),
    # Production
    path('production/unit/add/',
         ProductionUnitCreateView.as_view(), name="create_unit"),
    path('production/unit/detail/<pk>/',
         ProductionuUnitDetail.as_view(), name="detail_unit"),
    path('production/unit/update/<pk>/',
         ProductionUnitUpdate.as_view(), name="update_unit"),
    path('production/unit/delete/<pk>/',
         ProductionUnitDelete.as_view(), name="delete_unit"),
    path('production/unit/List/',
         ProductionUnitList.as_view(), name="list_unit"),

    # Species
    path('species/add', SpeciesCreateView.as_view(), name="create_specie"),
    path('species/detail/<pk>/', SpeciesDetail.as_view(), name="detail_specie"),
    path('species/update/<pk>/', SpeciesUpdate.as_view(), name="update_specie"),
    path('species/delete/<pk>/', SpeciesDelete.as_view(), name="delete_specie"),
    path('species/list/', SpeciesList.as_view(), name="list_specie"),

    path('<type>/', TracingInspectionHomeView.as_view(), name="tracing_home"),
    path('lagoon/<uuid:pk>', InspectionProductionUnitLagoon.as_view(),
         name="inspection_lagoon_list"),

    path('tracing/add/<pk>',
         TracingCreate.as_view(), name="create_tracing"),
    path('tracing/detail/<pk>/', TracingDetail.as_view(), name="detail_tracing"),
    path('tracing/update/<pk>/', TracingUpdate.as_view(), name="update_tracing"),
    path('tracing/delete/<pk>/', TracingdeleteView.as_view(), name="delete_tracing"),
    # path('list/', TracingList.as_view(), name="list_tracing"),
    path('well/detail/<pk>/', WellDetail.as_view(), name="well_detail"),
    path('lagoon/detail/<uuid:pk>/', LagoonDetail.as_view(), name="lagoon_detail"),

    path('legal/representative/<pk>/',
         RepreUnitCreate.as_view(), name="repre_create"),

    path('legal/representative/detail/<pk>/',
         Representative_unit_production_detail.as_view(), name="repre_detail"),

    path('legal/representative/delete/<pk>/',
         Representative_unit_production_delete.as_view(), name="repre_delete"),
    path('legal/representative/update/<pk>/',
         RepresentativeUnitProductionUpdate.as_view(), name="repre_update"),

]
