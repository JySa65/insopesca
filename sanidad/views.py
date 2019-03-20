from django.shortcuts import render, get_object_or_404
from django.core import serializers
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.views.generic import TemplateView, ListView, CreateView, \
    DetailView, UpdateView, DeleteView, View
from django.urls import reverse_lazy, reverse
from django.db.models import Q
from utils.check_password import checkPassword
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import timedelta, datetime
from sanidad import models, forms
import json
# Create your views here.


class InspectionDetailApiView(View):
    model = models.Inspection

    def get(self, *args, **kwargs):
        pk = self.request.GET.get('pk')
        queryset = get_object_or_404(self.model, pk=pk)
        data = dict(
            name=queryset.company_account.get_full_name(),
            date=queryset.date,
            result=queryset.result,
            next_date=queryset.next_date,
            notes=queryset.notes
        )
        return JsonResponse(data)


class InspectionListApiView(View):
    model = models.Inspection

    def get(self, *args, **kwargs):
        start = self.request.GET.get('start', '')
        end = self.request.GET.get('end', '')
        queryset = self.model.objects.filter(
            next_date__range=(start, end))
        data = []
        if queryset.count() != 0:
            for i in queryset:
                data.append(
                    dict(
                        pk=i.pk,
                        next_date=i.next_date,
                        result=i.result,
                        name=i.company_account.get_full_name()
                    )
                )
        return JsonResponse(data, safe=False)


class HomeTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'sanidad/home_view.html'


class CompanyListView(LoginRequiredMixin, ListView):
    model = models.Company

    def get_queryset(self):
        super(CompanyListView, self).get_queryset()
        return self.model.objects.filter(is_delete=False)


class TypeCompanyView(LoginRequiredMixin, View):
    model = models.TypeCompany

    def post(self, *args, **kwargs):
        try:
            name = json.loads(str(self.request.body, 'utf-8')).get('data', "")
            if name == "":
                data = dict(
                    status=False,
                    msg="Tipo De Compañia Requerido"
                )
                return JsonResponse(data)

            check_data = self.model.objects.filter(name=name.lower()).exists()
            if check_data:
                data = dict(
                    status=False,
                    msg="Tipo De Compañia Existe"
                )
                return JsonResponse(data)

            save_name = self.model.objects.create(name=name.lower())
            data = dict(
                status=True,
                msg="Tipo De Compañia Registrado",
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


class CompanyDetailView(LoginRequiredMixin, DetailView):
    model = models.Company

    def get_object(self):
        pk = self.kwargs.get('pk')
        object = self.model.objects.filter(is_delete=False, pk=pk).first()
        if self.request.user.is_superuser:
            object = get_object_or_404(self.model, pk=pk)
        elif not object:
            raise Http404
        return object


class CompanyCreateView(LoginRequiredMixin, CreateView):
    model = models.Company
    form_class = forms.CompanyForm

    def get_success_url(self):
        return reverse_lazy('sanidad:company_detail', args=(self.object.pk,))


class CompanyUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Company
    form_class = forms.CompanyForm

    def get_success_url(self):
        return reverse_lazy('sanidad:company_detail', args=(self.object.pk,))


class CompanyDeleteView(LoginRequiredMixin, View):
    model = models.Company

    def get_object(self):
        return get_object_or_404(
            models.Company, pk=self.kwargs.get('pk'))

    def delete(self, request, *args, **kwargs):
        company = self.get_object()
        company.is_delete = True
        company.is_active = False
        company.save()
        data = dict(
            status=True,
            msg="Empresa Eliminada"
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


class AccoutCompanyCreateView(LoginRequiredMixin, CreateView):
    model = models.Account
    form_class = forms.AccountForm
    template_name = 'sanidad/account_form.html'

    def get_object(self):
        return get_object_or_404(models.Company, pk=self.kwargs.get('pk'))

    def get_account_company(self, **data):
        company = data.get('company')
        user = data.get('user')
        return models.CompanyHasAccount.objects.filter(
            account=user, company=company).exists()

    def get_context_data(self, *args, **kwargs):
        context = super(AccoutCompanyCreateView,
                        self).get_context_data(**kwargs)
        company = self.get_object()

        context['company'] = company
        search = self.request.GET.get('search', '')
        if search != '':
            user = self.model.objects.filter(document=search).first()
            if user:
                user_exists = self.get_account_company(
                    user=user, company=company)
                if user_exists:
                    context['message'] = "Persona Ya Existe En La Empresa"
                else:
                    context['account'] = user
        return context

    def post(self, *args, **kwargs):
        company = self.get_object()
        form = self.form_class(self.request.POST)
        add = self.request.POST.get('add', "")
        ci = self.request.POST.get('document', "")
        if add != "":
            try:
                user = self.model.objects.get(pk=add)
                user_exists = self.get_account_company(
                    user=user, company=company)
                if not user_exists:
                    data = dict(
                        company=company,
                        account=user
                    )
                    models.CompanyHasAccount.objects.create(**data)
                    return HttpResponseRedirect(
                        reverse_lazy('sanidad:company_detail', args=(company.pk,)))
            except self.model.DoesNotExist:
                return HttpResponseRedirect(
                    reverse_lazy('sanidad:company_detail', args=(company.pk,)))
        user = self.model.objects.filter(document=ci)
        if user.exists():
            user_exists = self.get_account_company(
                user=user.first(), company=company)
            if not user_exists:
                data = dict(
                    company=company,
                    account=user
                )
                models.CompanyHasAccount.objects.create(**data)
                return HttpResponseRedirect(
                    reverse_lazy('sanidad:company_detail', args=(company.pk,)))
            return render(self.request, self.template_name, {
                'form': form, 'company': company})

        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            data = dict(
                company=company,
                account=user
            )
            models.CompanyHasAccount.objects.create(**data)
            return HttpResponseRedirect(
                reverse_lazy('sanidad:company_detail', args=(company.pk,)))
        return render(self.request, self.template_name, {
            'form': form, 'company': company})


class AccoutCompanyDetailView(LoginRequiredMixin, DetailView):
    model = models.Account
    pk_url_kwarg = 'account'

    def get_context_data(self, **kwargs):
        context = super(AccoutCompanyDetailView,
                        self).get_context_data(**kwargs)
        context['company'] = models.Company.objects.filter(
            pk=self.kwargs.get('pk')).first()
        context['account_has'] = models.CompanyHasAccount.objects.filter(
            company__pk=self.kwargs.get('pk'),
            account__pk=self.kwargs.get('account')).first()
        return context


class AccountCompanyUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Account
    form_class = forms.AccountForm
    pk_url_kwarg = 'account'
    template_name = 'sanidad/account_form.html'

    def get_context_data(self, **kwargs):
        context = super(AccountCompanyUpdateView,
                        self).get_context_data(**kwargs)
        context['edit'] = True
        context['company'] = self.getCompany()
        return context

    def form_valid(self, form):
        password = self.request.POST.get('password', '')
        user = checkPassword(self.request.user.email, password)
        if not user:
            return render(self.request, self.template_name, {
                'form': form, 'company': self.getCompany(), 'message': "Contraseña Incorrecta", 'edit': True})
        return super(AccountCompanyUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('sanidad:account_detail', args=(self.kwargs.get('pk'), self.object.pk))

    def getCompany(self):
        return models.Company.objects.filter(
            pk=self.kwargs.get('pk')).first()


class AccountCompanyDeleteView(LoginRequiredMixin, View):
    model = models.Company

    def get_object(self):
        return get_object_or_404(
            models.Company, pk=self.kwargs.get('pk'))

    def delete(self, request, *args, **kwargs):
        company = self.get_object()
        account = models.CompanyHasAccount.objects.filter(
            company=company,
            account__id=self.kwargs.get('account')).first()
        account.account_active = not account.account_active
        account.save()
        data = dict(
            status=True,
            msg="Usuario Desactivado" if not account.account_active else "Usuario Activado"
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


class TransportCompanyCreateView(LoginRequiredMixin, CreateView):
    model = models.Transport
    template_name = 'sanidad/transport_form.html'

    def get_object(self):
        return get_object_or_404(models.Company, pk=self.kwargs.get('pk'))

    def dispatch(self, request, *args, **kwargs):
        type_transport = self.kwargs.get('type')
        if (type_transport != 'land' and
            type_transport != 'maritime' and
                type_transport != 'fluvial'):
            raise Http404
        return super(
            TransportCompanyCreateView, self).dispatch(
                request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(TransportCompanyCreateView,
                        self).get_context_data(**kwargs)
        context['company'] = self.get_object()
        context['type_transport'] = self.kwargs.get('type')
        return context

    def form_valid(self, form):
        _object = form.save(commit=False)
        pk = self.kwargs.get('pk')
        data = get_object_or_404(models.Company, pk=pk)
        _object.type = f'is_{self.kwargs.get("type")}'
        _object.company_driver = data
        self.object = _object.save()
        return super(TransportCompanyCreateView, self).form_valid(form)

    def get_form(self, form_class=None):
        form_class = forms.TransportLandForm
        if self.kwargs.get("type") == 'maritime':
            form_class = forms.TransportMaritimeForm
        if self.kwargs.get('type') == 'fluvial':
            form_class = forms.TransportFluvialForm
        return form_class(**self.get_form_kwargs())

    def get_success_url(self):
        return reverse_lazy('sanidad:company_detail', args=(
            self.kwargs.get('pk'),))


class InspectionCreateView(LoginRequiredMixin, CreateView):
    model = models.Inspection
    form_class = forms.InspectionForm
    success_url = reverse_lazy('sanidad:inspection_list')

    def get_context_data(self, **kwargs):
        context = super(InspectionCreateView, self).get_context_data(**kwargs)
        q = self.request.GET.get('q', '')
        if q != '':
            company = models.Company.objects.filter(
                Q(name__iexact=q) | Q(document=q)).first()
            driver = models.Driver.objects.filter(
                document=q).first()
            if company or driver:
                inspection = models.Inspection.objects.filter(
                    company_account_id=company.pk if company else driver.pk if driver else None
                ).exclude(created_at__lte=timezone.now() - timedelta(365)
                          ).filter(next_date__gte=timezone.now())
                if not inspection:
                    context['data'] = company if company else driver
                    context['data_type'] = 'company' if company else 'driver'
                else:
                    msg = company if company else driver
                    context['message'] = f'{msg.get_full_name()} Ya Fue Inspeccionado(a)'
            else:
                context['message'] = 'No existe lo que esta buscando'
        return context

    def form_valid(self, form):
        pk = self.request.POST.get('token')
        _object = form.save(commit=False)
        try:
            data = models.Company.objects.get(pk=pk)
            _object.company_account = data
        except Exception:
            try:
                data = models.Driver.objects.get(pk=pk)
                _object.company_account = data
            except Exception:
                raise Http404
        self.object = _object.save()
        return super(InspectionCreateView, self).form_valid(form)


class InspectionListView(LoginRequiredMixin, ListView):
    model = models.Inspection
    paginate_by = 30


class InspectionDetailView(LoginRequiredMixin, DetailView):
    model = models.Inspection


class DriverListView(LoginRequiredMixin, ListView):
    model = models.Driver


class DriverDetailView(LoginRequiredMixin, DetailView):
    model = models.Driver


class DriverCreateView(LoginRequiredMixin, CreateView):
    model = models.Driver
    form_class = forms.DriverForm
    success_url = reverse_lazy('sanidad:driver_list')

    def get_context_data(self, *args, **kwargs):
        context = super(DriverCreateView,
                        self).get_context_data(**kwargs)
        search = self.request.GET.get('search', '')
        try:
            context['account'] = self.model.objects.get(document=search)
        except self.model.DoesNotExist:
            pass
        return context


class DriverUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Driver
    form_class = forms.DriverForm

    def get_context_data(self, **kwargs):
        context = super(DriverUpdateView,
                        self).get_context_data(**kwargs)
        context['edit'] = True
        return context

    def get_success_url(self):
        return reverse_lazy('sanidad:driver_detail', args=(self.object.pk,))


class DriverDeleteView(LoginRequiredMixin, View):
    model = models.Driver

    def delete(self, request, *args, **kwargs):
        user = get_object_or_404(self.model, pk=self.kwargs.get('pk'))
        user.is_active = not user.is_active
        user.save()
        data = {}
        data = dict(
            status=True,
            msg="Usuario Desactivado" if not user.is_active else "Usuario Activado"
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


class TransportDriverCreateView(LoginRequiredMixin, CreateView):
    model = models.Transport
    template_name = 'sanidad/transport_form.html'

    def get_object(self):
        return get_object_or_404(models.Driver, pk=self.kwargs.get('pk'))

    def dispatch(self, request, *args, **kwargs):
        type_transport = self.kwargs.get('type')
        if (type_transport != 'land' and
            type_transport != 'maritime' and
                type_transport != 'fluvial'):
            raise Http404
        return super(
            TransportDriverCreateView, self).dispatch(
                request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(TransportDriverCreateView,
                        self).get_context_data(**kwargs)
        context['company'] = self.get_object()
        context['type_transport'] = self.kwargs.get('type')
        return context

    def form_valid(self, form):
        _object = form.save(commit=False)
        data = self.get_object()
        _object.type = f'is_{self.kwargs.get("type")}'
        _object.company_driver = data
        self.object = _object.save()
        return super(TransportDriverCreateView, self).form_valid(form)

    def get_form(self, form_class=None):
        form_class = forms.TransportLandForm
        if self.kwargs.get("type") == 'maritime':
            form_class = forms.TransportMaritimeForm
        if self.kwargs.get('type') == 'fluvial':
            form_class = forms.TransportFluvialForm
        return form_class(**self.get_form_kwargs())

    def get_success_url(self):
        return reverse_lazy('sanidad:driver_detail', args=(
            self.kwargs.get('pk'),))
