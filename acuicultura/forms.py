from django import forms
from acuicultura.models import ProductionUnit, CardinalPoint, RepreUnitProductive, \
    Specie, Tracing, InspectionLagoon, BoundaryMap, StatusInsopesca
from django.db.models import Q


class UnitCreateForm(forms.ModelForm):
    tlf = forms.CharField(max_length=11, required=True,)
    tlf_house = forms.CharField(max_length=11, required=True)

    class Meta:
        model = ProductionUnit
        fields = ('name',
                  'tlf', 'tlf_house', 'state', 'municipality',
                  'parish', 'address')


class CardinaPointForm(forms.ModelForm):

    class Meta:
        model = CardinalPoint
        fields = ("north_utm", "west_utm",
                  "altitude", "total_area_terr")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update(
                {'id': f'id_{name}_utm'})


class BoundaryMapForm(forms.ModelForm):

    class Meta:
        model = BoundaryMap
        exclude = ('production_unit',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs.update(
                {'class': 'form-control', 'autocomplete': 'off'})


class EspecieForm(forms.ModelForm):
    class Meta:
        model = Specie
        fields = ('ordinary_name',
                  'scientific_name')

    def clean(self):
        cleaned_data = super(EspecieForm, self).clean()
        ordinary_name = cleaned_data['ordinary_name']
        scientific_name = cleaned_data['scientific_name']

        if not ordinary_name and not scientific_name:
            msg = "Al Menos Debe Ingresar un Nombre sea Cientifico o Ordinario"
            self.add_error('ordinary_name', msg)

        if ordinary_name or scientific_name:
            specie = Specie.objects.filter(
                Q(ordinary_name=ordinary_name) | Q(scientific_name=scientific_name))

            if specie.exists():
                data = specie.first()
                spes = data.ordinary_name if data.ordinary_name else data.scientific_name
                msg = f"Especie {spes} Ya Existe"
                self.add_error('ordinary_name', msg)

        return cleaned_data


class TracingCreateForm(forms.ModelForm):

    class Meta:
        model = Tracing
        fields = ('number_lagoon', 'new_number_lagoon', 
                'number_well', 'new_number_well',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs.update(
                {'class': 'form-control', 'autocomplete': 'off'})


class TracingUpdateForm(forms.ModelForm):
    class Meta:
        model = Tracing
        fields = ('number_lagoon', 'new_number_lagoon', 
                'number_well', 'new_number_well')

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.fields['new_number_lagoon'].widget.attrs['readonly'] = 'readonly'


class RepresentativeForm(forms.ModelForm):

    class Meta:
        model = RepreUnitProductive
        fields = ("type_document", "document", "name",
                  "last_name", "tlf", "tlf_house", 'address')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update(
                {'class': 'form-control', 'autocomplete': 'off'})

            if name == 'type_document':
                field.widget.attrs.update(
                    {'class': 'form-control selectpicker show-tick', 'autocomplete': 'off'})

            if name == "address":
                field.widget.attrs.update(
                    {'class': 'form-control', 'autocomplete': 'off', 'rows': 1})


class InspectionLagoonForm(forms.ModelForm):

    class Meta:
        model = InspectionLagoon
        exclude = ('user',
                   'lagoon',
                   'next_date')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update(
                {'class': 'form-control', 'autocomplete': 'off'})

            if name == "notes":
                field.widget.attrs.update(
                    {'class': 'form-control', 'autocomplete': 'off', 'rows': 1})


class StatusInsopescaForm(forms.ModelForm):

    class Meta:
        model = StatusInsopesca
        exclude = ('company',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs.update(
                {'class': 'custom-control-input'})
