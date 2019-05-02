from django import forms
from acuicultura.models import ProductionUnit, CardinalPoint, RepreUnitProductive, Specie, Tracing
from django.db.models import Q


class UnitCreateForm(forms.ModelForm):
    tlf = forms.CharField(max_length=11, required=True,)
    tlf_house = forms.CharField(max_length=11, required=True)

    class Meta:
        model = ProductionUnit
        fields = ('type_document', 'document', 'name',
                  'tlf', 'tlf_house', 'state', 'municipality',
                  'parish', 'address')


class CardinaPointForm(forms.ModelForm):

    class Meta:
        model = CardinalPoint
        fields = ("north", "south", "west", "oest",
                  "altitude", "total_area_terr")


class RepreUnitForm(forms.ModelForm):
    # phone_repre = forms.CharField(max_length=11,required=True,label="Telefono")
    # landline_repre = forms.CharField(max_length=11,required=True,label="Telefono Casa")

    class Meta:
        model = RepreUnitProductive
        fields = ("type_document", "document", "name",
                  "last_name", "tlf", "tlf_house")


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
        fields = ('number_lagoon', 'new_number_lagoon', 'number_well', 'new_number_well',
                  'illegal_superfaces', 'irregular_superfaces', 'permise_superfaces', 'regular_superfaces')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs.update(
                {'class': 'form-control', 'autocomplete': 'off'})


class TracingUpdateForm(forms.ModelForm):
    class Meta:
        model = Tracing
        fields = ('number_lagoon', 'new_number_lagoon', 'number_well', 'new_number_well',
                  'illegal_superfaces', 'irregular_superfaces', 'permise_superfaces', 'regular_superfaces')

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.fields['new_number_lagoon'].widget.attrs['readonly'] = 'readonly'


class RepresentativeForm(forms.ModelForm):
    class Meta:
        model = RepreUnitProductive
        fields = ("type_document", "document", "name",
                  "last_name", "tlf", "tlf_house")
