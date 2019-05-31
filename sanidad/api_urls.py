from django.urls import path
from sanidad.api_views import ChartMonthReportAPIView, ChartInspectionsDriverAndCompany, \
    ChartInspectionsType


app_name = 'sanidad'

urlpatterns = [
    path('chart_month/',
         ChartMonthReportAPIView.as_view(),
         name="chart_month_report"),

    path('chart_inspection_driver_company/',
         ChartInspectionsDriverAndCompany.as_view(),
         name="chart_inspection_driver_company"),

    path('chart_inspection_type/',
         ChartInspectionsType.as_view(),
         name="chart_inspection_type"),
]
