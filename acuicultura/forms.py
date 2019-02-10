from django import forms
from acuicultura.models import Production_unit,Cardinal_point,Repre_unit_productive


class UnitCreateForm(forms.ModelForm):
    class Meta:
        model = Production_unit
        fields = ('type_document','document','name','landline','phone','operative','municipality','state','parish')


class CardinaPointForm(forms.ModelForm):
    class Meta:
        model = Cardinal_point
        fields =  ("north", "south", "west", "oest", "altitude","total_area_terr")

class RepreUnitForm(forms.ModelForm):
    class Meta:
        model = Repre_unit_productive
        fields = ("type_document_repre","document_repre","name_repre","last_name_repre","landline_repre","phone_repre")
