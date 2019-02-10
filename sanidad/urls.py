from django.urls import path
from sanidad.views import HomeTemplateView, \
    CompanyListView, CompanyCreateView, CompanyDetailView, CompanyUpdateView

app_name = 'sanidad'

urlpatterns = [
    path('', HomeTemplateView.as_view(), name="home"),
    path('company/', CompanyListView.as_view(), name="company_list"),
    path('company/add/', CompanyCreateView.as_view(), name="company_create"),
    path('company/detail/<pk>/', CompanyDetailView.as_view(), name="company_detail"),
    path('company/update/<pk>/', CompanyUpdateView.as_view(), name="company_update"),
]
