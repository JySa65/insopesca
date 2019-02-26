from django import forms
from sanidad.models import Company, Account, Transport
from utils.Select import Selects


class CompanyForm(forms.ModelForm):
    speg = forms.CharField(label='SPEG')
    
    class Meta:
        model = Company
        fields = ('type_document', 'document', 'speg', 'type_company',
                'name', 'tlf','state', 'municipality',
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
        exclude = ('is_active', 'is_delete')

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
                {'class': 'form-control', 'autocomplete': 'off', 'required':'required'})


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
