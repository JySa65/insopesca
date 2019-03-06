from django import forms
from django.shortcuts import get_object_or_404
from sanidad.models import Company, Account, Transport, Inspection
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


def get_company_not_check():
    date = timezone.now()-timedelta(days=365)
    companys = Company.objects.all()
    a = []
    for company in companys:
        result = company.inspection_set.all().exclude(
            created_at__lte=(date)).filter(
            next_date__lte=timezone.now())
        print(result)
        if result.count() != 0:
            a.append((company.pk, company.name))
            
    return a


class InspectionForm(forms.ModelForm):
    company = forms.ChoiceField(
        choices=get_company_not_check()
    )

    class Meta:
        model = Inspection
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.get_company_not_check()
        for _, field in self.fields.items():
            field.widget.attrs.update(
                {'class': 'form-control', 'autocomplete': 'off'})
        self.fields['notes'].widget.attrs.update(
            {'rows': '1'})
        self.fields['company'].widget.attrs.update(
            {'class': 'form-control', 'data-live-search': 'true',
             'data-width': "100%", 'data-show-subtext': "true"})

    def clean_company(self):
        data = self.cleaned_data['company']
        return get_object_or_404(Company, pk=data)
