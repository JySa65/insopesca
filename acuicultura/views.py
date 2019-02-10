from django.shortcuts import render
from acuicultura.models import Production_unit, Species, Tracing, Repre_unit_productive, Cardinal_point
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View, TemplateView, DetailView
from acuicultura.forms import UnitCreateForm, CardinaPointForm, RepreUnitForm
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.core.paginator import Paginator
# Create your views here.


class AcuiculturaHome(ListView):
    template_name = "acuicultura/home.html"
    model = Production_unit

    def get_queryset(self):
        super(AcuiculturaHome, self).get_queryset()
        return self.model.objects.filter(is_delete=False).order_by("-id")[:5]


# Views Production = Create,detail,update,delete

class ProductionUnitCreateView(CreateView):
    model = Production_unit
    second_model = Cardinal_point
    three_model = Repre_unit_productive
    form_class = UnitCreateForm
    second_form = CardinaPointForm
    three_form = RepreUnitForm
    template_name = "acuicultura/production_unit_form.html"

    def form_valid(self, form):
        _object = form.save(commit=False)
        self.object = _object.save()
        return super(ProductionUnitCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'first' not in context:
            context["first"] = self.form_class()

        if 'second' not in context:
            context["second"] = self.second_form()

        if 'three' not in context:
            context["three"] = self.three_form()

        return context

    def post(self, request, *args, **kwargs):
        unit_form = self.form_class(request.POST)
        cardinal_form = self.second_form(request.POST)
        representative_form = self.three_form(request.POST)
        if unit_form.is_valid() and cardinal_form.is_valid() and representative_form.is_valid():
            unit_save = unit_form.save()
            cardinal = cardinal_form.save(commit=False)
            cardinal.production_unit_id = unit_save.pk

            representative = representative_form.save(commit=False)
            representative.production_unit_id = unit_save.pk
            cardinal_form.save()
            representative_form.save()
            return redirect("acuicultura:home")
        else:
            return render(request, self.template_name, {'form': unit_form, 'second': cardinal_form, "three": representative_form})


class ProductionUnitList(ListView):
    model = Production_unit
    template_name = "acuicultura/product_list.html"

    def get_context_data(self, **kwargs):
        context = super(ProductionUnitList, self).get_context_data(**kwargs)
        context['data'] = self.model.objects.all()
        paginator = Paginator(context['data'], 30)
        page = self.request.GET.get('page')
        context['object_list'] = paginator.get_page(page)
        return context


class ProductionUnitUpdate(UpdateView):
    model = Production_unit
    second_model = Cardinal_point
    three_model = Repre_unit_productive
    form_class = UnitCreateForm
    second_form = CardinaPointForm
    three_form = RepreUnitForm

    template_name = "acuicultura/production_unit_form.html"

    def form_valid(self, form):
        _object = form.save(commit=False)
        self.object = _object.save()
        return super(ProductionUnitUpdate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ProductionUnitUpdate, self).get_context_data(**kwargs)
        unit = self.model.objects.filter(pk=self.kwargs['pk']).first()
        cardinal = self.second_model.objects.filter(
            production_unit=self.kwargs['pk']).first()
        representative = self.three_model.objects.filter(
            production_unit=self.kwargs['pk']).first()
        if 'first' not in context:
            context['first'] = self.form_class(instance=unit)

        if 'second' not in context:
            context["second"] = self.second_form(instance=cardinal)

        if 'three' not in context:
            context["three"] = self.three_form(instance=representative)

        return context

    def post(self, request, *args, **kwargs):
        unit = self.model.objects.get(pk=self.kwargs['pk'])
        cardinal = self.second_model.objects.filter(
            production_unit=self.kwargs['pk']).first()
        unit_form = self.form_class(request.POST, instance=unit)
        cardinal_form = self.second_form(request.POST, instance=cardinal)
        representative = self.three_model.objects.filter(
            production_unit=self.kwargs['pk']).first()
        representative_form = self.three_form(
            request.POST, instance=representative)

        if unit_form.is_valid() and cardinal_form.is_valid() and representative_form.is_valid():
            unit_form.save()
            cardinal_form.save()
            representative_form.save()

            return redirect("acuicultura:home")
        else:
            print("invalido")
            return render(request, self.template_name, {'form': unit_form, 'second': cardinal_form, "three": representative_form})


class ProductionuUnitDetail(DetailView):
    model = Production_unit
    template_name = "acuicultura/unit_detail.html"

    def get_context_data(self, **kwargs):
        context = super(ProductionuUnitDetail, self).get_context_data(**kwargs)
        context['cardinal'] = get_object_or_404(
            Cardinal_point, production_unit=self.kwargs['pk'])
        context['representative'] = get_object_or_404(
            Repre_unit_productive, production_unit=self.kwargs['pk'])
        return context


class ProductionUnitDelete(DeleteView):
    model = Production_unit
    template_name = "acuicultura/product_confirm_delete.html"

    def post(self, request, *args, **kwargs):
        unit = self.model.objects.get(pk=self.kwargs['pk'])
        print(unit.is_delete)
        unit.is_delete = True
        unit.operative = False

        unit.save()
        return redirect("acuicultura:home")
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
