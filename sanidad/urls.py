from django.urls import path
from sanidad.views import HomeTemplateView, \
    CompanyListView, CompanyCreateView, CompanyDetailView, \
    CompanyUpdateView, CompanyDeleteView, AccoutCompanyCreateView, \
    AccoutCompanyDetailView, AccountCompanyUpdateView, AccountCompanyDeleteView

app_name = 'sanidad'

urlpatterns = [
    path('', HomeTemplateView.as_view(), name="home"),
    path('company/', CompanyListView.as_view(), name="company_list"),
    path('company/add/', CompanyCreateView.as_view(), name="company_create"),
    path('company/detail/<pk>/', CompanyDetailView.as_view(), name="company_detail"),
    path('company/update/<pk>/', CompanyUpdateView.as_view(), name="company_update"),
    path('company/delete/<pk>/', CompanyDeleteView.as_view(), name="company_delete"),

    path('company/detail/<pk>/account/',
         AccoutCompanyCreateView.as_view(), name="account_create"),
    path('company/detail/<pk>/account/detail/<account>',
         AccoutCompanyDetailView.as_view(), name="account_detail"),
    path('company/detail/<pk>/account/update/<account>',
         AccountCompanyUpdateView.as_view(), name="account_update"),
    path('company/detail/<pk>/account/update/<account>',
         AccountCompanyUpdateView.as_view(), name="account_update"),
    path('company/detail/<pk>/account/delete/<account>',
         AccountCompanyDeleteView.as_view(), name="account_delete")
]
