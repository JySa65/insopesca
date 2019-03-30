from django.urls import path
from reports import sanidad as sanidad_views
app_name = 'reports'

urlpatterns = [
    path('sanidad/inspection/list',
    sanidad_views.ReportSanidadListInpections.as_view(),
    name="sanidad_inspection_list"
    )
]
