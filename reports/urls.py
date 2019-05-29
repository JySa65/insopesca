from django.urls import path
from reports import sanidad as sanidad_views
from reports import sanidad_excel as sanidad_excel_views
app_name = 'reports'

urlpatterns = [
    path('sanidad/inspection/list',
         sanidad_views.ReportSanidadListInpections.as_view(),
         name="sanidad_inspection_list"),

    path('sanidad/report/company/all/',
         sanidad_views.ReportListCompanyOrDriver.as_view(),
         name="sanidad_report_all_company"),

    path('sanidad/excel/inspection/',
         sanidad_excel_views.InpectionsCompany.as_view(),
         name="sanidad_inspection_excel_report"),

    path('sanidad/report/list/',
         sanidad_views.ReportListCompanyOrDriver.as_view(),
         name="sanidad_report_list"),

    path('sanidad/report/individual/',
         sanidad_views.ReportIndividualCompanyOrDriver.as_view(),
         name="sanidad_individual"),
]
