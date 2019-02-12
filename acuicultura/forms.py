from django import forms
from acuicultura.models import ProductionUnit, CardinalPoint, RepreUnitProductive,Specie,Tracing


class UnitCreateForm(forms.ModelForm):
    tlf = forms.CharField(max_length=11,required=True,)
    tlf_house = forms.CharField(max_length=11,required=True)

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
    phone_repre = forms.CharField(max_length=11,required=True,label="Telefono")
    landline_repre = forms.CharField(max_length=11,required=True,label="Telefono Casa")

    class Meta:
        model = RepreUnitProductive
        fields = ("type_document_repre", "document_repre", "name_repre",
                  "last_name_repre", "landline_repre", "phone_repre")

class EspecieForm(forms.ModelForm):
    class Meta:
        model = Specie
        fields = ('__all__')


class TracingForm(forms.ModelForm):
    class Meta:
        model = Tracing
        fields = ('number_lagoon','new_number_lagoon','number_well','new_number_well','illegal_superfaces','irregular_superfaces','permise_superfaces','regular_superfaces')

class RepresentativeForm(forms.ModelForm):
    class Meta:
        model = RepreUnitProductive
        fields = ("type_document_repre","document_repre","name_repre","last_name_repre","landline_repre","phone_repre")
        