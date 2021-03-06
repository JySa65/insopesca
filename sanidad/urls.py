from django.urls import path
from sanidad.views import HomeTemplateView, \
    CompanyListView, CompanyCreateView, CompanyDetailView, \
    CompanyUpdateView, CompanyDeleteView, AccoutCompanyCreateView, \
    AccoutCompanyDetailView, AccountCompanyUpdateView, AccountCompanyDeleteView, \
    TransportCompanyCreateView, TypeCompanyView, \
    InspectionCreateView, InspectionListView, InspectionDetailView, \
    DriverListView, DriverDetailView, DriverCreateView, DriverUpdateView, \
    DriverDeleteView, TransportDriverCreateView, InspectionListApiView, \
    InspectionDetailApiView, InspectionListNotificationView, \
    InspectionDriversCompanyListView, ReportGenreralView, ReportGeneralAPIView, \
    UglyReportsView, ReportInspectionExpired, HomeGrapichView, TypeCompanyListView

app_name = 'sanidad'

urlpatterns = [
    path('', HomeTemplateView.as_view(), name="home"),
    path('type-company/', TypeCompanyView.as_view(), name="type_company"),

    path('company/', CompanyListView.as_view(), name="company_list"),
    path('company/add/', CompanyCreateView.as_view(), name="company_create"),
    path('company/detail/<pk>/', CompanyDetailView.as_view(), name="company_detail"),
    path('company/update/<pk>/', CompanyUpdateView.as_view(), name="company_update"),
    path('company/delete/<pk>/', CompanyDeleteView.as_view(), name="company_delete"),


    path('company/detail/<pk>/account/',
         AccoutCompanyCreateView.as_view(), name="account_create"),
    path('company/detail/<pk>/account/detail/<account>/',
         AccoutCompanyDetailView.as_view(), name="account_detail"),
    path('company/detail/<pk>/account/update/<account>/',
         AccountCompanyUpdateView.as_view(), name="account_update"),
    path('company/detail/<pk>/account/update/<account>/',
         AccountCompanyUpdateView.as_view(), name="account_update"),
    path('company/detail/<pk>/account/delete/<account>/',
         AccountCompanyDeleteView.as_view(), name="account_delete"),


    path('company/detail/<pk>/transport/<str:type>',
         TransportCompanyCreateView.as_view(), name="transport_create"),

    path('inspection/api/list/',
         InspectionListApiView.as_view(),
         name="inspection_api_list"),

    path('inspection/api/detail/',
         InspectionDetailApiView.as_view(),
         name="inspection_api_detail"),


    path('inspection/',
         InspectionListView.as_view(), name="inspection_list"),
    path('inspection/create/',
         InspectionCreateView.as_view(), name="inspection_create"),
    path('inspection/<pk>/',
         InspectionDetailView.as_view(), name="inspection_detail"),

    path('inspection/list/<type>',
         InspectionDriversCompanyListView.as_view(),
         name="inspection_drivers_company"),

    path('driver/', DriverListView.as_view(), name="driver_list"),
    path('driver/create/', DriverCreateView.as_view(), name="driver_create"),
    path('driver/detail/<pk>/', DriverDetailView.as_view(), name="driver_detail"),
    path('driver/update/<pk>/', DriverUpdateView.as_view(), name="driver_update"),
    path('driver/delete/<pk>/', DriverDeleteView.as_view(), name="driver_delete"),
    path('driver/detail/<pk>/transport/<str:type>',
         TransportDriverCreateView.as_view(), name="transport_driver"),

    path('notification/',
         InspectionListNotificationView.as_view(),
         name='notification'),

    path('report/',
         ReportGenreralView.as_view(),
         name="report_views"),

     path('api/report/',
          ReportGeneralAPIView.as_view(),
          name="api_report_views"),

     path('api/report/inspections',
          ReportInspectionExpired.as_view(),
          name="api_report_inspection"),


     path('sanidad/reports/<str:tip>/',
               UglyReportsView.as_view(),
          name="reports_sanidad"),

     # graphical

     path('graficos/', HomeGrapichView.as_view(), name="home_grapich"),

     # type company
     path('type_company/', TypeCompanyListView.as_view(), name="type_company")
]
