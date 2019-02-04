from django.shortcuts import render
from acuicultura.models import Production_unit,Species,Tracing,Repre_unit_productive
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View, TemplateView, DetailView

# Create your views here.


class UnitHomeView(ListView):
    template_name = "acuicultura/home.html"
    model = Production_unit

    def get_queryset(self):
        super(UnitHomeView, self).get_queryset()
        return self.model.objects.all().order_by("-id")[:5]

# Views Production = Create,detail,update,delete

# class Production_unit_CreateView(TemplateView):
#     model = Production_unit
#     template_name = "acuicultura/production_unit_form.html"


# class Production_unit_List(TemplateView):
#     model = Production_unit
#     template_name = "acuicultura/production_unit_form.html"

# class Production_unit_Update(TemplateView):
#     model = Production_unit
#     template_name = "acuicultura/production_unit_form.html"


# class Production_unit_Detail(TemplateView):
#     model = Production_unit
#     template_name = "acuicultura/production_unit_detail.html"


# class Production_unit_Delete(TemplateView):
#     model = Production_unit
#     template_name = "acuicultura/production_unit_delete.html"


# # Views Species = Create,detail,update,delete

# class SpeciesCreateView(TemplateView):
#     model = Species
#     template_name = "acuicultura/specie_form.html"


# class SpeciesList(TemplateView):
#     model = Species
#     template_name = "acuicultura/specie_form.html"


# class SpeciesUpdate(TemplateView):
#     model = Species
#     template_name = "acuicultura/specie_form.html"


# class SpeciesDetail(TemplateView):
#     model = Species
#     template_name = "acuicultura/specie_form.html"


# class SpeciesDelete(TemplateView):
#     model = Species
#     template_name = "acuicultura/specie_form.html"


# # Views Tracing = Create,detail,update,delete
# class TracingCreate(TemplateView):
#     model = Tracing
#     tempalte_name = "acuicultura/tracing_form.html"


# class TracingList(TemplateView):
#     model = Tracing
#     tempalte_name = "acuicultura/tracing_form.html"




# class TracingUpdate(TemplateView):
#     model = Tracing
#     tempalte_name = "acuicultura/tracing_form.html"


# class TracingDetail(TemplateView):
#     model = Tracing
#     tempalte_name = "acuicultura/tracing_form.html"


# class Tracingdelete(TemplateView):
#     model = Tracing
#     tempalte_name = "acuicultura/tracing_form.html"

# # Views Representative Unit

# class Representative_unit_production_create(TemplateView):
#     model = Repre_unit_productive 
#     template_name = "acuicultura/representative_form.html"


# class Representative_unit_production_update(TemplateView):
#     model = Repre_unit_productive 
#     template_name = "acuicultura/representative_form.html"


# class Representative_unit_production_delete(TemplateView):
#     model = Repre_unit_productive 
#     template_name = "acuicultura/representative_form.html"

# class Representative_unit_production_list(TemplateView):
#     model = Repre_unit_productive 
#     template_name = "acuicultura/representative_form.html"

# class Representative_unit_production_detail(TemplateView):
#     model = Repre_unit_productive 
#     template_name = "acuicultura/representative_form.html"