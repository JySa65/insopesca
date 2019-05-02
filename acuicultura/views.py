from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from acuicultura.models import ProductionUnit, Specie, Tracing, RepreUnitProductive, CardinalPoint, Well, WellTracing, Lagoon, LagoonTracing, LagoonEspecies
from acuicultura.forms import UnitCreateForm, CardinaPointForm, RepreUnitForm, EspecieForm, TracingCreateForm, TracingUpdateForm, RepresentativeForm
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, Http404, JsonResponse, \
    HttpResponse
from django.views.generic import TemplateView, ListView, CreateView, \
    DetailView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from utils.check_password import checkPassword
from django.urls import reverse, reverse_lazy
import json
from utils.permissions import UserUrlCorrectMixin
from django.db import transaction

# Create your views here.


class AcuiculturaHome(LoginRequiredMixin, UserUrlCorrectMixin, ListView):
    model = ProductionUnit
    template_name = "acuicultura/home.html"

    def get_queryset(self):
        super(AcuiculturaHome, self).get_queryset()
        return self.model.objects.all()[:5]

# Views Production = Create,detail,update,delete


class ProductionUnitCreateView(LoginRequiredMixin, UserUrlCorrectMixin, CreateView):
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


class ProductionUnitUpdate(LoginRequiredMixin, UserUrlCorrectMixin, UpdateView):
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
            return HttpResponseRedirect(reverse('acuicultura:detail_unit', args=(unit.pk,)))
        else:
            return render(request, self.template_name, {'form': unit_form, 'second': cardinal_form})


class ProductionuUnitDetail(LoginRequiredMixin, UserUrlCorrectMixin, DetailView):
    model = ProductionUnit

    template_name = "acuicultura/unit_detail.html"

    def get_context_data(self, **kwargs):
        context = super(ProductionuUnitDetail, self).get_context_data(**kwargs)
        pk = self.kwargs['pk']
        context['cardinal'] = get_object_or_404(
            CardinalPoint, production_unit=pk)
        context['representative'] = RepreUnitProductive.objects.filter(
            production_unit=pk)
        context['tracing'] = Tracing.objects.filter(
            producion_unit=pk)
        return context


class ProductionUnitList(LoginRequiredMixin, UserUrlCorrectMixin, ListView):
    model = ProductionUnit
    template_name = "acuicultura/product_list.html"

    def get_context_data(self, **kwargs):
        context = super(ProductionUnitList, self).get_context_data(**kwargs)
        context['data'] = self.model.objects.all()
        context['paginator'] = Paginator(context['data'], 30)
        page = self.request.GET.get('page')
        context['object_list'] = context['paginator'].get_page(page)
        return context


class ProductionUnitDelete(LoginRequiredMixin, UserUrlCorrectMixin, View):
    model = ProductionUnit

    def get_object(self):
        return get_object_or_404(
            self.model, pk=self.kwargs.get('pk'))

    def delete(self, request, *args, **kwargs):
        unit_production = self.get_object()
        unit_production.delete()
        data = dict(
            status=True,
            msg="Unidad Productora Eliminada"
        )
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        try:
            password = json.loads(
                str(self.request.body, 'utf-8')).get('password', "")
            user = checkPassword(self.request.user.email, password)
            if not user:
                data = dict(
                    status=False,
                    msg="Contraseña Incorrecta"
                )
                return JsonResponse(data)
            return self.delete(request, *args, **kwargs)
        except Exception as e:
            data = dict(
                status=False,
                data=e
            )
            return JsonResponse(data)
# # Views Species = Create,detail,update,delete


class SpeciesCreateView(LoginRequiredMixin, UserUrlCorrectMixin, CreateView):
    model = Specie
    form_class = EspecieForm
    template_name = "acuicultura/specie_form.html"

    def get_success_url(self):
        return reverse_lazy('acuicultura:list_specie')


class SpeciesList(LoginRequiredMixin, UserUrlCorrectMixin, ListView):
    model = Specie
    template_name = "acuicultura/specie_list.html"
    paginate_by = 30

    def get_context_data(self, **kwargs):
        context = super(SpeciesList, self).get_context_data(**kwargs)
        context['data'] = self.model.objects.all()
        context['paginator'] = Paginator(context['data'], 30)
        page = self.request.GET.get('page')
        context['object_list'] = context['paginator'].get_page(page)
        return context


class SpeciesUpdate(LoginRequiredMixin, UserUrlCorrectMixin, UpdateView):
    model = Specie
    form_class = EspecieForm
    template_name = "acuicultura/specie_form.html"

    def get_success_url(self):
        return reverse_lazy('acuicultura:detail_specie', args=(self.object.id,))


class SpeciesDetail(LoginRequiredMixin, UserUrlCorrectMixin, DetailView):
    model = Specie
    template_name = "acuicultura/specie_detail.html"


class SpeciesDelete(LoginRequiredMixin, UserUrlCorrectMixin, View):
    model = Specie

    def get_object(self):
        return get_object_or_404(
            self.model, pk=self.kwargs.get('pk'))

    def delete(self, request, *args, **kwargs):
        species = self.get_object()
        species.delete()
        data = dict(
            status=True,
            msg="Especie Eliminada"
        )
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        try:
            password = json.loads(
                str(self.request.body, 'utf-8')).get('password', "")
            user = checkPassword(self.request.user.email, password)
            if not user:
                data = dict(
                    status=False,
                    msg="Contraseña Incorrecta"
                )
                return JsonResponse(data)
            return self.delete(request, *args, **kwargs)
        except Exception as e:
            data = dict(
                status=False,
                data=e
            )
            return JsonResponse(data)


# # Views Tracing = Create,detail,update,delete
class TracingCreate(LoginRequiredMixin, UserUrlCorrectMixin, CreateView):
    model = Tracing
    form_class = TracingCreateForm
    tempalte_name = "acuicultura/tracing_form.html"

    def get_object(self):
        pk = self.kwargs['pk']
        return get_object_or_404(ProductionUnit, pk=pk)

    def get_context_data(self, **kwargs):
        context = super(TracingCreate, self).get_context_data(**kwargs)
        context['tracing_lagoon'] = LagoonTracing.objects.filter(
            tracing__producion_unit=self.get_object())

        context['tracing_well'] = WellTracing.objects.filter(
            tracing__producion_unit=self.get_object())
        context['current'] = self.get_object()
        context['species'] = [dict(
            id=i.pk,
            name=f"{i.scientific_name if i.scientific_name else '----'} - {i.ordinary_name if i.ordinary_name else '-----'}",
        ) for i in Specie.objects.all()]
        return context

    def post(self, request, *args, **kwargs):
        data = json.loads(str(request.body, 'utf-8'))
        lagoons = data.get('lagoon')
        wells = data.get('well')
        illegal_superfaces = data.get('illegal_superfaces', 0)
        irregular_superfaces = data.get('irregular_superfaces', 0)
        permise_superfaces = data.get('permise_superfaces', 0)
        regular_superfaces = data.get('regular_superfaces', 0)
        well_current = data.get('well_current', 0)
        laggon_current = data.get('laggon_current', 0)
        producion_unit = self.get_object()

        if len(lagoons) != 0:
            for number, lagoon in enumerate(lagoons):
                diameter = lagoon.get('diameter', '')
                deepth = lagoon.get('deepth', '')
                sistem_cultive = lagoon.get('sistem_cultive', None)
                _type = sistem_cultive.get('type', '')
                species = sistem_cultive.get('species', [])

                if (diameter == '' or deepth == '' or sistem_cultive == None):
                    data = dict(
                        status=False,
                        msg=f"Algunos Datos Son Requeridos En La Laguna N° {number+1}"
                    )
                    return JsonResponse(data)

                if _type == '':
                    data = dict(
                        status=False,
                        msg=f"Falta Añadir El Tipo De Sistema De Cultivo En La Laguna N° {number+1}"
                    )
                    return JsonResponse(data)

                if (_type == 'mono' and len(species) == 0 or
                        _type == 'duo' and len(species) <= 1):
                    data = dict(
                        status=False,
                        msg=f"Hace Falta Añadir La Especie En La Laguna N° {number+1}"
                    )
                    return JsonResponse(data)
                
                for _, specie in enumerate(species):
                    name = specie.get('specie', 0)
                    number_specie = specie.get('number_specie', 0)
                    
                    if (name == 0 or number_specie == 0):
                        data = dict(
                            status=False,
                            msg=f"Hace Falta Añadir La Especie o La Cantidad En La Laguna N° {number+1}"
                            )
                        return JsonResponse(data)

        if len(wells) != 0:
            for number, well in enumerate(wells):
                diameter = well.get('diameter', '')
                deepth = well.get('deepth', '')

                if (diameter == '' or deepth == ''):
                    data = dict(
                        status=False,
                        msg=f"Algunos Datos Son Requeridos En El Pozo N° {number+1}"
                    )
                    return JsonResponse(data)

        if (illegal_superfaces == 0 or irregular_superfaces == 0 or
                permise_superfaces == 0 or regular_superfaces == 0):
            data = dict(
                status=False,
                msg=f"Algunos Datos Son Requeridos En La Superficies"
            )
            return JsonResponse(data)

        try:
            with transaction.atomic():
                data = dict(
                    illegal_superfaces=illegal_superfaces,
                    irregular_superfaces=irregular_superfaces,
                    permise_superfaces=permise_superfaces,
                    regular_superfaces=regular_superfaces,
                    number_well=well_current,
                    number_lagoon=laggon_current,
                    new_number_lagoon=len(lagoons),
                    new_number_well=len(wells),
                    producion_unit=producion_unit,
                    responsible=request.user
                )
                tracing = Tracing.objects.create(**data)
                for lagoon in lagoons:
                    laggon = Lagoon.objects.create(
                        producion_unit=producion_unit,
                        lagoon_diameter=lagoon['diameter'],
                        lagoon_deepth=lagoon['deepth'],
                        sistem_cultivate=lagoon['sistem_cultive']['type'])

                    LagoonTracing.objects.create(
                        tracing=tracing, lagoon=laggon)
                 
                    for specie in lagoon['sistem_cultive']['species']:
                        pk = specie['specie']
                        number_specie = int(specie['number_specie'])
                        sspecie = get_object_or_404(Specie, pk=pk)
                        LagoonEspecies.objects.create(
                            lagoon=laggon,
                            especies=sspecie,
                            number_specie=number_specie)
                
                for well in wells:
                    welll = Well.objects.create(
                        producion_unit=producion_unit, 
                        well_diameter=well['diameter'], 
                        well_deepth=well['deepth'])

                    WellTracing.objects.create(
                            tracing=tracing, well=welll)
            data = dict(
                status=True,
                msg="Guardado Exitosamente"
            )
            return JsonResponse(data)
        except Exception as e:
            data = dict(
                status=False,
                msg=e
            )
            return JsonResponse(data)    
        
# class TracingList(TemplateView):
#     model = Tracing
#     tempalte_number_specie = "acuicultura/tracing_form.html"


class TracingUpdate(LoginRequiredMixin, UserUrlCorrectMixin, UpdateView):
    model = Tracing
    form_class = TracingUpdateForm

    tempalte_name = "acuicultura/tracing_form.html"

    def get_context_data(self, **kwargs):
        context = super(TracingUpdate, self).get_context_data(**kwargs)
        tracing = self.model.objects.filter(pk=self.kwargs['pk']).first()
        well_data = WellTracing.objects.filter(
            tracing=self.kwargs['pk']).order_by('-id')
        lagoon_data = LagoonTracing.objects.filter(
            tracing=self.kwargs['pk']).order_by('-id')
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
            lagoons = LagoonTracing.objects.filter(tracing=self.kwargs['pk'])

            if tracing_form.is_valid():
                tracing_form.save()
                cont = 0
                for j in lagoons:
                    a = Lagoon.objects.filter(pk=j.lagoon.pk).update(
                        lagoon_diameter=c_new_lagoon_diameter[cont], lagoon_deepth=c_new_lagoon_deepth[cont])
                    cont += 1
                return HttpResponseRedirect(reverse('acuicultura:detail_unit', args=(tracing.producion_unit.pk,)))

            else:
                return render(request, self.tempalte_name, {'form': form, 'new_well_diameter': json_new_well_diameter, 'new_well_deepth': json_new_well_deepth, 'new_lagoon_deepth': json_new_lagoon_deepth, 'new_lagoon_diameter': json_new_lagoon_diameter})

        else:
            return render(request, self.tempalte_name, {'form': form, 'new_well_diameter': json_new_well_diameter, 'new_well_deepth': json_new_well_deepth, 'new_lagoon_deepth': json_new_lagoon_deepth, 'new_lagoon_diameter': json_new_lagoon_diameter})


class TracingDetail(LoginRequiredMixin, UserUrlCorrectMixin, DetailView):
    model = Tracing
    tempalte_name = "acuicultura/tracing_detail.html"

    def get_context_data(self, **kwargs):
        context = super(TracingDetail, self).get_context_data(**kwargs)
        context['well_tracing'] = WellTracing.objects.filter(
            tracing=self.kwargs['pk'])
        context['lagoon_tracing'] = LagoonTracing.objects.filter(
            tracing=self.kwargs['pk'])

        return context


class WellDetail(LoginRequiredMixin, UserUrlCorrectMixin, DetailView):
    model = Well
    template_name = "acuicultura/detail_well.html"


class LagoonDetail(LoginRequiredMixin, UserUrlCorrectMixin, DetailView):
    model = Lagoon
    template_name = "acuicultura/detail_lagoon.html"

    def get_context_data(self, **kwargs):
        context = super(LagoonDetail, self).get_context_data(**kwargs)
        area = Lagoon.objects.filter(pk=self.kwargs['pk']).first()
        context['species_has_lagoon'] = LagoonEspecies.objects.filter(
            lagoon=self.kwargs['pk'])
        # # context['total_number_species'] = LagoonEspecies.objects.filter(
        # #     lagoon=self.kwargs['pk']).aggregate(total__sum=Sum('number_specie'))
        # context['square_meter'] = (area.lagoon_diameter*area.lagoon_deepth)
        # context['food'] = int((context['square_meter'])*1.5)
        # context['food_sacks'] = int((context['food'])/25)
        # context['percentage_60'] = (context['food_sacks'])*60/100
        # context['percentage_40'] = (context['food_sacks'])*40/100
        return context


class TracingdeleteView(View, UserUrlCorrectMixin, LoginRequiredMixin):
    model = Tracing

    def get_object(self):
        return get_object_or_404(
            self.model, pk=self.kwargs.get('pk'))

    def delete(self, request, *args, **kwargs):
        tracing = self.get_object()
        tracing.delete()
        data = dict(
            status=True,
            msg="Seguimiento Eliminado"
        )
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        try:
            password = json.loads(
                str(self.request.body, 'utf-8')).get('password', "")
            user = checkPassword(self.request.user.email, password)
            if not user:
                data = dict(
                    status=False,
                    msg="Contraseña Incorrecta"
                )
                return JsonResponse(data)
            return self.delete(request, *args, **kwargs)
        except Exception as e:
            data = dict(
                status=False,
                data=e
            )
            return JsonResponse(data)


# # Views Representative Unit

class RepreUnitCreate(LoginRequiredMixin, UserUrlCorrectMixin, CreateView):
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


class Representative_unit_production_detail(DetailView, UserUrlCorrectMixin):
    model = RepreUnitProductive
    template_name = "acuicultura/representative_detail.html"


class Representative_unit_production_delete(LoginRequiredMixin,
                                            UserUrlCorrectMixin, View):
    model = RepreUnitProductive

    def get_object(self):
        return get_object_or_404(
            self.model, pk=self.kwargs.get('pk'))

    def delete(self, request, *args, **kwargs):
        repre = self.get_object()
        repre.is_active = False
        repre.save()
        data = dict(
            status=True,
            msg="Representante Desactivado"
        )
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        try:
            password = json.loads(
                str(self.request.body, 'utf-8')).get('password', "")
            user = checkPassword(self.request.user.email, password)
            if not user:
                data = dict(
                    status=False,
                    msg="Contraseña Incorrecta"
                )
                return JsonResponse(data)
            return self.delete(request, *args, **kwargs)
        except Exception as e:
            data = dict(
                status=False,
                data=e
            )
            return JsonResponse(data)

# class Representative_unit_production_list(TemplateView):
#     model = RepreUnitProductive
#     template_name = "acuicultura/representative_form.html"


class RepresentativeUnitProductionUpdate(LoginRequiredMixin,
                                         UserUrlCorrectMixin, UpdateView):
    model = RepreUnitProductive
    form_class = RepresentativeForm
    template_name = "acuicultura/representative_form.html"

    def get_context_data(self, **kwargs):
        context = super(RepresentativeUnitProductionUpdate,
                        self).get_context_data(**kwargs)
        repre = self.model.objects.filter(
            production_unit=self.kwargs['pk']).first()
        if 'form' not in context:
            context['form'] = self.form_class(instance=repre)
        return context

    def post(self, request, *args, **kwargs):
        repre = self.model.objects.get(pk=self.kwargs['pk'])
        repre_form = self.form_class(request.POST, instance=repre)

        if repre_form.is_valid():
            repre_form.save()
            return HttpResponseRedirect(reverse("acuicultura:detail_unit", args=(repre.production_unit.pk,)))
        else:
            return render(self.request, self.template_name, {'form': form})
