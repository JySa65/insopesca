from django import forms
from django.shortcuts import get_object_or_404
from sanidad.models import Company, Account, Transport, Inspection, Driver
from utils.Select import Selects
from django.utils import timezone
from datetime import timedelta


class CompanyForm(forms.ModelForm):
    speg = forms.CharField(label='SPEG')

    class Meta:
        model = Company
        fields = ('type_document', 'document', 'speg', 'type_company',
                  'name', 'tlf', 'state', 'municipality',
                  'parish', 'address',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs.update(
                {'class': 'form-control', 'autocomplete': 'off'})
        self.fields['address'].widget.attrs.update(
            {'rows': '2'})


class AccountForm(forms.ModelForm):

    class Meta:
        model = Account
        exclude = ('is_active', 'is_delete', 'tlf_house')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs.update(
                {'class': 'form-control', 'autocomplete': 'off'})
        self.fields['address'].widget.attrs.update(
            {'rows': '1'})


class DriverForm(forms.ModelForm):

    class Meta:
        model = Driver
        exclude = ('is_active', 'is_delete', 'tlf_house')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs.update(
                {'class': 'form-control', 'autocomplete': 'off'})
        self.fields['address'].widget.attrs.update(
            {'rows': '1'})


class TransportLandForm(forms.ModelForm):

    class Meta:
        model = Transport
        fields = ('registration', 'model', 'brand', 'load_capacity')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs.update(
                {'class': 'form-control', 'autocomplete': 'off', 'required': 'required'})


class TransportMaritimeForm(forms.ModelForm):

    class Meta:
        model = Transport
        fields = ('name', 'year_vessel')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs.update(
                {'class': 'form-control', 'autocomplete': 'off',
                 'required': 'required'})


class InspectionForm(forms.ModelForm):

    class Meta:
        model = Inspection
        exclude = ('company_account_type', 'company_account_id',
                   'company_account')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs.update(
                {'class': 'form-control', 'autocomplete': 'off'})
        self.fields['notes'].widget.attrs.update(
            {'rows': '1'})

    # def clean_company(self):
    #     data = self.cleaned_data['company']
    #     return get_object_or_404(Company, pk=data)
