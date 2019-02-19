from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View, TemplateView, DetailView
from acuicultura.models import ProductionUnit, Specie, Tracing, RepreUnitProductive, CardinalPoint, Well, WellTracing, Lagoon, LagoonTracing
from acuicultura.forms import UnitCreateForm, CardinaPointForm, RepreUnitForm, EspecieForm, TracingForm, RepresentativeForm
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
import json

# Create your views here.


class AcuiculturaHome(ListView):
    model = ProductionUnit
    template_name = "acuicultura/home.html"

    def get_context_data(self, **kwargs):
        context = super(AcuiculturaHome, self).get_context_data(**kwargs)
        context['object_list'] = self.model.objects.all()[:5]
        return context


# Views Production = Create,detail,update,delete

class ProductionUnitCreateView(CreateView):
    model = ProductionUnit
    second_model = CardinalPoint
    form_class = UnitCreateForm
    second_form = CardinaPointForm
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

        return context

    def post(self, request, *args, **kwargs):
        unit_form = self.form_class(request.POST)
        cardinal_form = self.second_form(request.POST)

        if unit_form.is_valid() and cardinal_form.is_valid():
            unit_save = unit_form.save()
            cardinal = cardinal_form.save(commit=False)
            cardinal.production_unit_id = unit_save.pk
            cardinal_form.save()
            return HttpResponseRedirect(reverse('acuicultura:detail_unit', args=(unit_save.pk,)))

        else:
            return render(request, self.template_name, {'form': unit_form, 'second': cardinal_form})


class ProductionUnitUpdate(UpdateView):
    model = ProductionUnit
    second_model = CardinalPoint
    form_class = UnitCreateForm
    second_form = CardinaPointForm

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
        if 'first' not in context:
            context['first'] = self.form_class(instance=unit)

        if 'second' not in context:
            context["second"] = self.second_form(instance=cardinal)

        return context

    def post(self, request, *args, **kwargs):
        unit = self.model.objects.get(pk=self.kwargs['pk'])
        cardinal = self.second_model.objects.filter(
            production_unit=self.kwargs['pk']).first()
        unit_form = self.form_class(request.POST, instance=unit)
        cardinal_form = self.second_form(request.POST, instance=cardinal)

        if unit_form.is_valid() and cardinal_form.is_valid():
            unit_form.save()
            cardinal_form.save()
            return HttpResponseRedirect(reverse('acuicultura:detail_unit', args=(unit_save.pk,)))
        else:
            return render(request, self.template_name, {'form': unit_form, 'second': cardinal_form})


class ProductionuUnitDetail(DetailView):
    model = ProductionUnit

    template_name = "acuicultura/unit_detail.html"

    def get_context_data(self, **kwargs):
        context = super(ProductionuUnitDetail, self).get_context_data(**kwargs)
        context['cardinal'] = get_object_or_404(
            CardinalPoint, production_unit=self.kwargs['pk'])
        context['representative'] = RepreUnitProductive.objects.filter(
            production_unit=self.kwargs['pk'])
        context['tracing'] = Tracing.objects.filter(
            producion_unit=self.kwargs['pk'])
        return context


class ProductionUnitList(ListView):
    model = ProductionUnit
    template_name = "acuicultura/product_list.html"

    def get_context_data(self, **kwargs):
        context = super(ProductionUnitList, self).get_context_data(**kwargs)
        context['data'] = self.model.objects.all()
        context['paginator'] = Paginator(context['data'], 30)
        page = self.request.GET.get('page')
        context['object_list'] = context['paginator'].get_page(page)
        return context


class ProductionUnitDelete(DeleteView):
    model = ProductionUnit
    template_name = "acuicultura/product_confirm_delete.html"

    def post(self, request, *args, **kwargs):
        unit = self.model.objects.get(pk=self.kwargs['pk'])
        unit.is_delete = True
        unit.operative = False

        unit.save()
        return redirect("acuicultura:home")
# # Views Species = Create,detail,update,delete


class SpeciesCreateView(CreateView):
    model = Specie
    form_class = EspecieForm
    template_name = "acuicultura/specie_form.html"

    def get_success_url(self):
        return reverse_lazy('acuicultura:detail_specie', args=(self.object.id,))


class SpeciesList(ListView):
    model = Specie
    template_name = "acuicultura/specie_list.html"

    def get_context_data(self, **kwargs):
        context = super(SpeciesList, self).get_context_data(**kwargs)
        context['data'] = self.model.objects.all()
        context['paginator'] = Paginator(context['data'], 30)
        page = self.request.GET.get('page')
        context['object_list'] = context['paginator'].get_page(page)
        return context


class SpeciesUpdate(UpdateView):
    model = Specie
    form_class = EspecieForm
    template_name = "acuicultura/specie_form.html"

    def get_success_url(self):
        return reverse_lazy('acuicultura:detail_specie', args=(self.object.id,))


class SpeciesDetail(DetailView):
    model = Specie
    template_name = "acuicultura/specie_detail.html"


class SpeciesDelete(DeleteView):
    model = Specie
    template_name = "acuicultura/specie_delete.html"
    success_url = reverse_lazy('acuicultura:list_specie')


# # Views Tracing = Create,detail,update,delete
class TracingCreate(CreateView):
    model = Tracing
    form_class = TracingForm
    tempalte_name = "acuicultura/tracing_form.html"

    def form_valid(self, form):
        _object = form.save(commit=False)
        self.object = _object.save()
        return super(ProductionUnitUpdate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(TracingCreate, self).get_context_data(**kwargs)
        context['new_well_diameter'] = 0
        context['new_well_deepth'] = 0
        context['new_lagoon_diameter'] = 0
        context['new_lagoon_deepth'] = 0
        return context

    def post(self, request, *args, **kwargs):
        new_wells = request.POST.get("new_number_well", '')
        new_lagoon = request.POST.get("new_number_lagoon", '')
        unit = ProductionUnit.objects.filter(pk=self.kwargs['pk']).first()

        form = self.form_class(request.POST)
        c_new_well_deepth = []
        c_new_well_diameter = []
        c_new_lagoon_deepth = []
        c_new_lagoon_diameter = []
        for i in range(int(new_wells)):
            new_wells_diameter = request.POST.get(
                "new_wells_diameter_%s" % (i))
            new_wells_deepth = request.POST.get("new_wells_deepth_%s" % (i))
            if new_wells_diameter != None:
                c_new_well_diameter.append(new_wells_diameter)
                c_new_well_deepth.append(new_wells_deepth)

            json_new_well_diameter = json.dumps(c_new_well_diameter)
            json_new_well_deepth = json.dumps(c_new_well_deepth)

        for i in range(int(new_lagoon)):
            new_lagoon_diameter = request.POST.get(
                "new_lagoon_diameter_%s" % (i))
            new_lagoon_deepth = request.POST.get("new_lagoon_deepth_%s" % (i))
            if new_lagoon_diameter != None and new_lagoon_diameter != None:
                c_new_lagoon_deepth.append(new_lagoon_diameter)
                c_new_lagoon_diameter.append(new_lagoon_deepth)

            json_new_lagoon_diameter = json.dumps(c_new_lagoon_diameter)
            json_new_lagoon_deepth = json.dumps(c_new_lagoon_deepth)

        if form.is_valid():
            tracing = form.save(commit=False)
            tracing.producion_unit = unit
            tracing.responsible = request.user
            tracing.save()
            if request.POST.get("new_number_lagoon") != "0" and request.POST.get("new_number_well") == "0":

                for i in range(int(request.POST.get("new_number_well"))):
                    wells = Well.objects.create(
                        producion_unit=unit, well_diameter=c_new_well_diameter[i], well_deepth=c_new_well_deepth[i])
                    print(wells.pk)
                    print(tracing.pk)

                    wells_tracing = WellTracing.objects.create(
                        tracing=tracing, well=wells)
                return HttpResponseRedirect(reverse('acuicultura:detail_unit', args=(unit.pk,)))
            elif request.POST.get("new_number_well") != "0" and request.POST.get("new_number_lagoon") == "0":

                for i in range(int(request.POST.get("new_number_lagoon"))):
                    lagoon = Lagoon.objects.create(
                        producion_unit=unit, lagoon_diameter=c_new_lagoon_diameter[i], lagoon_deepth=c_ne[i])
                    print(lagoon.pk)
                    print(tracing.pk)

                    lagoon_tracing = WellTracing.objects.create(
                        tracing=tracing, well=lagoon)
                return HttpResponseRedirect(reverse('acuicultura:detail_unit', args=(unit.pk,)))

            elif request.POST.get("new_number_well") != "0" and request.POST.get("new_number_lagoon") != "0":

                for i in range(int(request.POST.get("new_number_well"))):
                    wells = Well.objects.create(
                        producion_unit=unit, well_diameter=c_new_well_diameter[i], well_deepth=c_new_well_deepth[i])
                    wells_tracing = WellTracing.objects.create(
                        tracing=tracing, well=wells)

                for i in range(int(request.POST.get("new_number_lagoon"))):
                    print(c_new_lagoon_diameter)
                    print(c_new_lagoon_deepth)
                    lagoon = Lagoon.objects.create(
                        producion_unit=unit, lagoon_diameter=c_new_lagoon_diameter[i], lagoon_deepth=c_new_lagoon_deepth[i])
                    lagoon_tracing = LagoonTracing.objects.create(
                        tracing=tracing, lagoon=lagoon)

                return HttpResponseRedirect(reverse('acuicultura:detail_unit', args=(unit.pk,)))
                print("ambos")
            else:
                return render(request, self.tempalte_name, {'form': form, 'new_well_diameter': json_new_well_diameter, 'new_well_deepth': json_new_well_deepth, 'new_lagoon_deepth': json_new_lagoon_deepth, 'new_lagoon_diameter': json_new_lagoon_diameter})

        else:
            return render(request, self.tempalte_name, {'form': form, 'new_well_diameter': json_new_well_diameter, 'new_well_deepth': json_new_well_deepth, 'new_lagoon_deepth': json_new_lagoon_deepth, 'new_lagoon_diameter': json_new_lagoon_diameter})

# class TracingList(TemplateView):
#     model = Tracing
#     tempalte_name = "acuicultura/tracing_form.html"


class TracingUpdate(UpdateView):
    model = Tracing
    form_class = TracingForm

    tempalte_name = "acuicultura/tracing_form.html"

    def get_context_data(self, **kwargs):
        context = super(TracingUpdate, self).get_context_data(**kwargs)
        tracing = self.model.objects.filter(pk=self.kwargs['pk']).first()
        well_data = WellTracing.objects.filter(
            tracing=self.kwargs['pk']).order_by('-id')
        lagoon_data = LagoonTracing.objects.filter(
            tracing=self.kwargs['pk']).order_by('-id')
        print(lagoon_data, "jajaja")
        if len(well_data) == 0:
            context['new_well_diameter'] = 0
            context['new_well_deepth'] = 0

        if len(lagoon_data) == 0:
            context['new_lagoon_diameter'] = 0
            context['new_lagoon_deepth'] = 0
        c_new_well_deepth = []
        c_new_well_diameter = []
        c_new_lagoon_deepth = []
        c_new_lagoon_diameter = []

        if 'form' not in context:
            context['form'] = self.form_class(instance=tracing)

        for i_well in well_data:
            c_new_well_diameter.append(i_well.well.well_diameter)
            c_new_well_deepth.append(i_well.well.well_deepth)

        for i_lagoon in lagoon_data:
            c_new_lagoon_diameter.append(i_lagoon.lagoon.lagoon_diameter)
            c_new_lagoon_deepth.append(i_lagoon.lagoon.lagoon_deepth)

        context['new_well_diameter'] = json.dumps(c_new_well_diameter)
        context['new_well_deepth'] = json.dumps(c_new_well_deepth)
        context['new_lagoon_diameter'] = json.dumps(c_new_lagoon_diameter)
        context['new_lagoon_deepth'] = json.dumps(c_new_lagoon_deepth)

        return context

    def post(self, request, *args, **kwargs):
        new_wells = request.POST.get("new_number_well", '')
        new_lagoon = request.POST.get("new_number_lagoon", '')
        unit = ProductionUnit.objects.filter(pk=self.kwargs['pk']).first()

        form = self.form_class(request.POST)

        c_new_well_deepth = []
        c_new_well_diameter = []
        c_new_lagoon_deepth = []
        c_new_lagoon_diameter = []

        for i in range(int(new_wells)):
            new_wells_diameter = request.POST.get(
                "new_wells_diameter_%s" % (i))
            new_wells_deepth = request.POST.get("new_wells_deepth_%s" % (i))
            if new_wells_diameter != None:
                c_new_well_diameter.append(new_wells_diameter)
                c_new_well_deepth.append(new_wells_deepth)

            json_new_well_diameter = json.dumps(c_new_well_diameter)
            json_new_well_deepth = json.dumps(c_new_well_deepth)

        for i in range(int(new_lagoon)):
            new_lagoon_diameter = request.POST.get(
                "new_lagoon_diameter_%s" % (i))
            new_lagoon_deepth = request.POST.get("new_lagoon_deepth_%s" % (i))
            if new_lagoon_diameter != None and new_lagoon_diameter != None:
                c_new_lagoon_deepth.append(new_lagoon_diameter)
                c_new_lagoon_diameter.append(new_lagoon_deepth)

            json_new_lagoon_diameter = json.dumps(c_new_lagoon_diameter)
            json_new_lagoon_deepth = json.dumps(c_new_lagoon_deepth)

        if form.is_valid():
            tracing = self.model.objects.get(pk=self.kwargs['pk'])

            tracing_form = self.form_class(request.POST, instance=tracing)

            if tracing_form.is_valid():
                tracing_form.save()
                return HttpResponseRedirect(reverse('acuicultura:detail_unit', args=(tracing.producion_unit.pk,)))

            else:
                return render(request, self.tempalte_name, {'form': form, 'new_well_diameter': json_new_well_diameter, 'new_well_deepth': json_new_well_deepth, 'new_lagoon_deepth': json_new_lagoon_deepth, 'new_lagoon_diameter': json_new_lagoon_diameter})

        else:
            return render(request, self.tempalte_name, {'form': form, 'new_well_diameter': json_new_well_diameter, 'new_well_deepth': json_new_well_deepth, 'new_lagoon_deepth': json_new_lagoon_deepth, 'new_lagoon_diameter': json_new_lagoon_diameter})


class TracingDetail(DetailView):
    model = Tracing
    tempalte_name = "acuicultura/tracing_detail.html"

    def get_context_data(self, **kwargs):
        context = super(TracingDetail, self).get_context_data(**kwargs)
        context['well_tracing'] = WellTracing.objects.filter(
            tracing=self.kwargs['pk'])
        context['lagoon_tracing'] = LagoonTracing.objects.filter(
            tracing=self.kwargs['pk'])

        return context

class WellDetail(DetailView):
    model = Well
    template_name = "acuicultura/detail_well.html"

class LagoonDetail(DetailView):
    model = Lagoon
    template_name = "acuicultura/detail_lagoon.html"


# class Tracingdelete(TemplateView):
#     model = Tracing
#     tempalte_name = "acuicultura/tracing_form.html"

# # Views Representative Unit

class RepreUnitCreate(CreateView):
    model = ProductionUnit
    second_model = RepreUnitProductive
    template_name = "acuicultura/representative_form.html"
    form_class = RepresentativeForm

    def form_valid(self, form):
        _object = form.save(commit=False)
        self.object = _object.save()
        return super(ProductionUnitUpdate, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        unit = self.model.objects.filter(pk=self.kwargs['pk']).first()
        repre = self.second_model.objects.filter(
            production_unit=self.kwargs['pk'])
        form = self.form_class(request.POST)

        if form.is_valid():
            repre = form.save(commit=False)
            repre.production_unit_id = unit.pk
            repre.save()
            return HttpResponseRedirect(reverse("acuicultura:detail_unit", args=(unit.pk,)))
        else:
            return render(self.request, self.template_name, {'form': form})


class RepresentativeUnitProduction(UpdateView):
    model = RepreUnitProductive
    second_model = RepreUnitProductive
    form_class = RepresentativeForm
    template_name = "acuicultura/representative_form.html"

    
    def get_context_data(self, **kwargs):
        context = super(RepresentativeUnitProduction, self).get_context_data(**kwargs)
        repre = self.model.objects.filter(production_unit=self.kwargs['pk']).first()
        if 'form' not in context:
            context['form'] = self.form_class(instance=repre)
        return context
    

    def post(self, request, *args, **kwargs):
        tracing = self.model.objects.get(pk=self.kwargs['pk'])

        tracing_form = self.form_class(request.POST, instance=tracing)

        if tracing_form.is_valid():
            tracing_form.save()
            return HttpResponseRedirect(reverse("acuicultura:detail_unit", args=(unit.pk,)))
        else:
            return render(self.request, self.template_name, {'form': form})


class Representative_unit_production_detail(TemplateView):
    model = RepreUnitProductive
    template_name = "acuicultura/representative_form.html"

# class Representative_unit_production_delete(TemplateView):
#     model = RepreUnitProductive
#     template_name = "acuicultura/representative_form.html"

# class Representative_unit_production_list(TemplateView):
#     model = RepreUnitProductive
#     template_name = "acuicultura/representative_form.html"