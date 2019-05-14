from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from acuicultura.models import ProductionUnit, Specie, Tracing, RepreUnitProductive, CardinalPoint, Well, WellTracing, Lagoon, LagoonTracing, LagoonEspecies, RepreUnitProductiveMany, BoundaryMap, BoundaryMapSelect, InspectionLagoon
from acuicultura.forms import UnitCreateForm, CardinaPointForm, EspecieForm, TracingCreateForm, TracingUpdateForm, RepresentativeForm, BoundaryMapForm, InspectionLagoonForm
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from django.db.models.functions import Lower
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
from django.utils import timezone
# Create your views here.


class AcuiculturaHome(LoginRequiredMixin, UserUrlCorrectMixin, ListView):
    model = ProductionUnit
    template_name = "acuicultura/home.html"

    def get_queryset(self):
        super(AcuiculturaHome, self).get_queryset()
        return self.model.objects.all()[:5]


class LinderoView(LoginRequiredMixin, UserUrlCorrectMixin, View):
    model = BoundaryMapSelect

    def post(self, *args, **kwargs):
        try:
            name = json.loads(str(self.request.body, 'utf-8')).get('data', "")
            if name == "":
                data = dict(
                    status=False,
                    msg="Lindero Requerido"
                )
                return JsonResponse(data)
            # print(name)

            # self.model.objects.filter(name=name)
            check_data = self.model.objects.filter(name=name).exists()
            if check_data:
                data = dict(
                    status=False,
                    msg="Lindero Ya Existe"
                )
                return JsonResponse(data)

            save_name = self.model.objects.create(name=name.lower())
            data = dict(
                status=True,
                msg="Lindero Registrado",
                data=dict(
                    id=save_name.id,
                    name=save_name.name
                )
            )
            return JsonResponse(data)
        except Exception as e:
            data = dict(
                status=False,
                data=e
            )
            return JsonResponse(data)


# Views Production = Create,detail,update,delete
class ProductionUnitCreateView(LoginRequiredMixin, UserUrlCorrectMixin, CreateView):
    model = ProductionUnit
    second_model = CardinalPoint
    thrid_model = BoundaryMap
    form_class = UnitCreateForm
    second_form = CardinaPointForm
    three_form = BoundaryMapForm
    template_name = "acuicultura/production_unit_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["first"] = self.form_class()
        context["second"] = self.second_form()
        context["three"] = self.three_form()
        return context

    def post(self, request, *args, **kwargs):
        unit_form = self.form_class(request.POST)
        utm_form = self.second_form(request.POST)
        location_form = self.three_form(request.POST)

        if unit_form.is_valid() and utm_form.is_valid() and location_form.is_valid():
            with transaction.atomic():
                unit_save = unit_form.save()
                utm = utm_form.save(commit=False)
                utm.production_unit_id = unit_save.pk
                location = location_form.save(commit=False)
                location.production_unit = unit_save
                utm.save()
                location.save()
                return HttpResponseRedirect(
                    reverse('acuicultura:detail_unit', args=(unit_save.pk,)))
        return render(
            request,
            self.template_name,
            {'form': unit_form, 'second': utm_form, 'three': location_form})


class ProductionUnitUpdate(LoginRequiredMixin, UserUrlCorrectMixin, UpdateView):
    model = ProductionUnit
    second_model = CardinalPoint
    thrid_model = BoundaryMap
    form_class = UnitCreateForm
    second_form = CardinaPointForm
    three_form = BoundaryMapForm
    template_name = "acuicultura/production_unit_form.html"


    def get_context_data(self, **kwargs):
        context = super(ProductionUnitUpdate, self).get_context_data(**kwargs)
        unit = self.object
        cardinal = self.second_model.objects.filter(
            production_unit=unit).first()
        linder = self.thrid_model.objects.filter(
             production_unit=unit).first()

        context['first'] = self.form_class(instance=unit)
        context["second"] = self.second_form(instance=cardinal)
        context["three"] = self.three_form(instance=linder)
        return context

    def post(self, request, *args, **kwargs):
        unit = get_object_or_404(self.model, pk=self.kwargs.get('pk'))
        cardinal = self.second_model.objects.filter(
            production_unit=unit).first()
        linder = self.thrid_model.objects.filter(
            production_unit=unit).first()
        unit_form = self.form_class(request.POST, instance=unit)
        cardinal_form = self.second_form(request.POST, instance=cardinal)
        linder_form = self.three_form(request.POST, instance=linder)
        if (unit_form.is_valid() and cardinal_form.is_valid() and
            linder_form.is_valid()):
            unit_form.save()
            cardinal_form.save()
            linder_form.save()
            return HttpResponseRedirect(
                reverse('acuicultura:detail_unit', args=(unit.pk,)))
        else:
            return render(request, 
                    self.template_name, 
                    {'form': unit_form, 'second': cardinal_form})


class ProductionuUnitDetail(LoginRequiredMixin, UserUrlCorrectMixin, DetailView):
    model = ProductionUnit

    template_name = "acuicultura/unit_detail.html"

    def get_context_data(self, **kwargs):
        context = super(ProductionuUnitDetail, self).get_context_data(**kwargs)
        context['cardinal'] = get_object_or_404(
            CardinalPoint, production_unit=self.object)
        context['linder'] = BoundaryMap.objects.filter(
            production_unit=self.object)
        context['representative'] = RepreUnitProductiveMany.objects.filter(
            production_unit=self.object)
        context['tracing'] = Tracing.objects.filter(
            producion_unit=self.object).order_by('-created_at')
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


class InspectionProductionUnitLagoon(LoginRequiredMixin, UserUrlCorrectMixin, ListView):
    model = Lagoon

    def get_queryset(self):
        super(InspectionProductionUnitLagoon, self).get_queryset()
        return Lagoon.objects.filter(producion_unit__pk=self.kwargs.get('pk'))


# # Views Tracing = Create,detail,update,delete
class TracingInspectionHomeView(LoginRequiredMixin, UserUrlCorrectMixin, TemplateView):
    template_name = "acuicultura/tracing_home.html"
    model = ProductionUnit

    def dispatch(self, request, *args, **kwargs):
        if self.kwargs.get('type') not in ['tracing', 'lagoon']:
            raise Http404
        return super(TracingInspectionHomeView,
                     self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(TracingInspectionHomeView,
                        self).get_context_data(**kwargs)
        query = self.request.GET.get('q', '')
        context['productionunits'] = []
        if query:
            data = self.model.objects.filter(name__startswith=query)
            if data:
                context['productionunits'] = data
            else:
                context['error'] = "No Hay Resultados"
        context['type'] = self.kwargs.get('type')
        return context


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
            name=f"{i.scientific_name if i.scientific_name else '----'} - {i.ordinary_name if i.ordinary_name else '----'}",
        ) for i in Specie.objects.all()]
        return context

    def post(self, request, *args, **kwargs):
        data = json.loads(str(request.body, 'utf-8'))
        print(data)
        lagoons = data.get('lagoon')
        wells = data.get('well')
        illegal_superfaces = data.get('illegal_superfaces', 0)
        permise_superfaces = data.get('permise_superfaces', 0)
        regular_superfaces = data.get('regular_superfaces', 0)
        well_current = data.get('well_current', 0)
        laggon_current = data.get('laggon_current', 0)
        producion_unit = self.get_object()

        if len(lagoons) != 0:
            for number, lagoon in enumerate(lagoons):
                diameter = lagoon.get('diameter', '')
                deepth = lagoon.get('deepth', '')
                height = lagoon.get('height', '')
                type_lagoon = lagoon.get('type', '')
                sistem_cultive = lagoon.get('sistem_cultive', None)
                _type = sistem_cultive.get('type', '')
                species = sistem_cultive.get('species', [])

                if (diameter == '' or deepth == '' or sistem_cultive == None or
                        height == '' or type_lagoon == ''):
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

        if (illegal_superfaces == 0 or
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
                        sistem_cultivate=lagoon['sistem_cultive']['type'],
                        lagoon_height=lagoon['height'],
                        lagoon_type=lagoon['type'])

                    LagoonTracing.objects.create(
                        tracing=tracing, lagoon=laggon)

                    for specie in lagoon['sistem_cultive']['species']:
                        pk = specie['specie']
                        number_specie = specie['number_specie']
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
        lagoon = self.object
        species = LagoonEspecies.objects.filter(lagoon=lagoon)

        # densidad de animales
        fish = species.aggregate(
            total=Sum('number_specie'))
        if fish['total'] == None:
            fish['total'] = 0

        area = lagoon.lagoon_diameter * lagoon.lagoon_deepth
        alevino = int(int(fish['total']) * area)

        # calculo alimenticio
        food = (alevino * 1.5)
        food_sacks = food / 25

        # percentage
        percentage_60 = (food_sacks*60)/100
        percentage_40 = (food_sacks*40)/100

        context['species'] = species
        context['total_number_species'] = fish['total']
        context['densidad'] = dict(
            area=int(area),
            alevino=int(alevino)
        )
        context['calculo'] = dict(
            food=int(food),
            food_sacks=round(food_sacks, 2)
        )
        context['percen'] = dict(
            percentage_60=round(percentage_60, 2),
            percentage_40=round(percentage_40, 2),
        )
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

    def dispatch(self, request, *args, **kwargs):
        get_object_or_404(self.model, pk=self.kwargs.get('pk'))
        return super(RepreUnitCreate, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        unit = get_object_or_404(self.model, pk=self.kwargs.get('pk'))
        form = self.form_class(request.POST)
        try:
            data_user = request.POST.get('user', '')
            if data_user:
                user = get_object_or_404(self.second_model, pk=data_user)
                RepreUnitProductiveMany.objects.create(
                    production_unit=unit, user=user)
                return HttpResponseRedirect(
                    reverse("acuicultura:detail_unit", args=(unit.pk,)))

            document = request.POST.get('document')
            user = self.second_model.objects.get(document=document)
            user_many = RepreUnitProductiveMany.objects.filter(
                production_unit=unit, user=user).exists()

            ctx = dict(
                form=form,
                user=user,
                msg="Usuario Ya Existe En El Sistema ¿Desea Añadirlo?",
                add=True
            )
            if user_many:
                ctx['msg'] = "Usuario Ya Existe En Esta Unidad Productora"
                ctx['add'] = False

            return render(self.request, self.template_name, ctx)
        except self.second_model.DoesNotExist:
            with transaction.atomic():
                if form.is_valid():
                    repre = form.save()
                    RepreUnitProductiveMany.objects.create(
                        production_unit=unit, user=repre)
                    return HttpResponseRedirect(
                        reverse("acuicultura:detail_unit", args=(unit.pk,)))
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
        self.get_object().delete()
        data = dict(
            status=True,
            msg="Representante Removido"
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


class RepresentativeUnitProductionUpdate(LoginRequiredMixin,
                                         UserUrlCorrectMixin, UpdateView):
    model = RepreUnitProductive
    form_class = RepresentativeForm
    template_name = "acuicultura/representative_form.html"

    def get_success_url(self):
        return reverse_lazy("acuicultura:repre_detail", args=(self.object.pk,))


class LagoonInspectionView(LoginRequiredMixin, UserUrlCorrectMixin, ListView):
    model = InspectionLagoon
    paginate_by = 10

    def get_queryset(self):
        queryset = super(LagoonInspectionView, self).get_queryset()
        queryset = queryset.filter(
            lagoon=self.kwargs.get('pk')).order_by('-date')
        return queryset

    
    def get_context_data(self, **kwargs):
        context = super(LagoonInspectionView, self).get_context_data(**kwargs)
        context['lagoon'] = get_object_or_404(Lagoon, pk=self.kwargs.get('pk'))
        return context


class LagoonInspectionCreateView(LoginRequiredMixin, UserUrlCorrectMixin, CreateView):
    model = InspectionLagoon
    form_class = InspectionLagoonForm
    
    def get_context_data(self, **kwargs):
        context = super(LagoonInspectionCreateView, self).get_context_data(**kwargs)
        context['lagoon'] = get_object_or_404(Lagoon, pk=self.kwargs.get('pk'))
        return context

    def form_valid(self, form):
        _object = form.save(commit=False)
        _object.user = self.request.user
        _object.lagoon = get_object_or_404(Lagoon, pk=self.kwargs.get('pk'))
        _object.next_date = timezone.now()
        _object.save()
        return super(LagoonInspectionCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'acuicultura:inspection_lagoon', args=(self.kwargs.get('pk'),))

    
