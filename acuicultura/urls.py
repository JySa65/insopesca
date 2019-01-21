from django.urls import path
from acuicultura.views import Home,Production_unit_CreateView,Production_unit_Update,Production_unit_List,Production_unit_Detail,Production_unit_Delete, \
                                        SpeciesCreateView,SpeciesDelete,SpeciesDetail,SpeciesList,SpeciesUpdate ,\
                                        TracingCreate,TracingDetail,TracingUpdate,Tracingdelete ,TracingList, \
                                        Representative_unit_production_create,Representative_unit_production_delete ,\
                                        Representative_unit_production_detail,Representative_unit_production_update,Representative_unit_production_list

app_name = "acuicultura"

urlpatterns = [

    path('',Home.as_view(),name="home"),
    # Production
    path('create/', Production_unit_CreateView.as_view(), name="create_unit"),
    path('detail/<pk>/', Production_unit_Detail.as_view(), name="detail_unit"),
    path('update/<pk>/', Production_unit_Update.as_view(), name="update_unit"),
    path('delete/<pk>/', Production_unit_Delete.as_view(), name="delete_unit"),
    path('list/', Production_unit_List.as_view(), name="list_unit"),


    path('create/', SpeciesCreateView.as_view(), name="create_specie"),
    path('detail/<pk>/', SpeciesDetail.as_view(), name="detail_specie"),
    path('update/<pk>/', SpeciesUpdate.as_view(), name="update_specie"),
    path('delete/<pk>/', SpeciesDelete.as_view(), name="delete_specie"),
    path('list/', SpeciesList.as_view(), name="list_specie"),



    path('create/', TracingCreate.as_view(), name="create"),
    path('detail/<pk>/', TracingDetail.as_view(), name="detail_tracing"),
    path('update/<pk>/', TracingUpdate.as_view(), name="update_tracing"),
    path('delete/<pk>/', Tracingdelete.as_view(), name="delete_tracing"),
    path('list/', TracingList.as_view(), name="list_tracing"),


    path('create/', Representative_unit_production_create.as_view(), name="create_repre"),
    path('detail/<pk>/', Representative_unit_production_detail.as_view(), name="detail_repre"),
    path('update/<pk>/', Representative_unit_production_update.as_view(), name="update_repre"),
    path('delete/<pk>/', Representative_unit_production_delete.as_view(), name="delete_repre"),
    path('list/', Representative_unit_production_detail.as_view(), name="list_specie_repre"),
    path('list/', Representative_unit_production_list.as_view(), name="list_tracing_repre"),


]