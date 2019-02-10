from django.urls import path
from acuicultura.views import AcuiculturaHome, ProductionUnitCreateView, ProductionUnitUpdate,\
    ProductionuUnitDetail, ProductionUnitDelete, ProductionUnitList


# ,Production_unit_CreateView,Production_unit_Update,Production_unit_List, \
# Production_unit_Detail,Production_unit_Delete,SpeciesCreateView,SpeciesDelete,SpeciesDetail, \
# SpeciesList,SpeciesUpdate,TracingCreate,TracingDetail,TracingUpdate,Tracingdelete ,TracingList, \
# Representative_unit_production_create,Representative_unit_production_delete,Representative_unit_production_list,\
# Representative_unit_production_detail,Representative_unit_production_update

app_name = "acuicultura"
urlpatterns = [

    path('', AcuiculturaHome.as_view(), name="home"),
    # Production
    path('Registrar/Unidad/Productora/',
         ProductionUnitCreateView.as_view(), name="create_unit"),
    path('Unidad/Productora/Detalles/<pk>/',
         ProductionuUnitDetail.as_view(), name="detail_unit"),
    path('Actualizar/Unidad/Productora/<pk>/',
         ProductionUnitUpdate.as_view(), name="update_unit"),
    path('Unidad/Productora/Eliminar/<pk>/',
         ProductionUnitDelete.as_view(), name="delete_unit"),
    path('Listado/Unidad/Productora/',
         ProductionUnitList.as_view(), name="list_unit"),


    # path('create/', SpeciesCreateView.as_view(), name="create_specie"),
    # path('detail/<pk>/', SpeciesDetail.as_view(), name="detail_specie"),
    # path('update/<pk>/', SpeciesUpdate.as_view(), name="update_specie"),
    # path('delete/<pk>/', SpeciesDelete.as_view(), name="delete_specie"),
    # path('list/', SpeciesList.as_view(), name="list_specie"),

    # path('create/', TracingCreate.as_view(), name="create"),
    # path('detail/<pk>/', TracingDetail.as_view(), name="detail_tracing"),
    # path('update/<pk>/', TracingUpdate.as_view(), name="update_tracing"),
    # path('delete/<pk>/', Tracingdelete.as_view(), name="delete_tracing"),
    # path('list/', TracingList.as_view(), name="list_tracing"),


]
