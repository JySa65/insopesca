from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.views.generic import TemplateView, ListView, CreateView, \
    DetailView, UpdateView, DeleteView, View
from django.urls import reverse_lazy, reverse
from django.db.models import Q
from utils.check_password import checkPassword
from django.utils import timezone
from datetime import timedelta
from sanidad import models, forms
import json
# Create your views here.


class HomeTemplateView(TemplateView):
    template_name = 'sanidad/home_view.html'


class CompanyListView(ListView):
    model = models.Company

    def get_queryset(self):
        super(CompanyListView, self).get_queryset()
        return self.model.objects.filter(is_delete=False)


class TypeCompanyView(View):
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


class CompanyDetailView(DetailView):
    model = models.Company

    def get_object(self):
        pk = self.kwargs.get('pk')
        object = self.model.objects.filter(is_delete=False, pk=pk).first()
        if self.request.user.is_superuser:
            object = get_object_or_404(self.model, pk=pk)
        elif not object:
            raise Http404
        return object


class CompanyCreateView(CreateView):
    model = models.Company
    form_class = forms.CompanyForm

    def get_success_url(self):
        return reverse_lazy('sanidad:company_detail', args=(self.object.pk,))


class CompanyUpdateView(UpdateView):
    model = models.Company
    form_class = forms.CompanyForm

    def get_success_url(self):
        return reverse_lazy('sanidad:company_detail', args=(self.object.pk,))


class CompanyDeleteView(View):
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


class AccoutCompanyCreateView(CreateView):
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


class AccoutCompanyDetailView(DetailView):
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


class AccountCompanyUpdateView(UpdateView):
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


class AccountCompanyDeleteView(View):
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


class TransportCompanyCreateView(CreateView):
    model = models.Transport
    template_name = 'sanidad/transport_form.html'

    def get_object(self):
        return get_object_or_404(models.Company, pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super(TransportCompanyCreateView,
                        self).get_context_data(**kwargs)
        context['company'] = self.get_object()
        type_transport = self.kwargs.get('type')
        if type_transport != 'land' and type_transport != 'maritime':
            raise Http404
        context['type_transport'] = type_transport
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
        if self.kwargs.get("type") != 'land':
            form_class = forms.TransportMaritimeForm
        return form_class(**self.get_form_kwargs())

    def get_success_url(self):
        return reverse_lazy('sanidad:company_detail', args=(
            self.kwargs.get('pk'),))


class InspectionCreateView(CreateView):
    model = models.Inspection
    form_class = forms.InspectionForm
    success_url = reverse_lazy('sanidad:inspection_list')

    def get_context_data(self, **kwargs):
        context = super(InspectionCreateView, self).get_context_data(**kwargs)
        q = self.request.GET.get('q', '')
        if q != '':
            company = models.Company.objects.filter(
                Q(name__iexact=q) | Q(document=q)).first()
            if company:
                inspection = models.Inspection.objects.filter(
                    company_account_id=company.pk).exclude(
                        created_at__lte=timezone.now() - timedelta(365)
                ).exclude(next_date__gte=timezone.now()
                          ).first()
                if not inspection:
                    context['data'] = company
                    context['data_type'] = 'company'
                else:
                    context['message'] = f'{company.name} Ya Fue Inspeccionado(a)'

        return context

    def form_valid(self, form):
        pk = self.request.POST.get('token')
        data = get_object_or_404(models.Company, pk=pk)
        _object = form.save(commit=False)
        _object.company_account = data
        self.object = _object.save()
        return super(InspectionCreateView, self).form_valid(form)


class InspectionListView(ListView):
    model = models.Inspection


class InspectionDetailView(DetailView):
    model = models.Inspection


class DriverListView(ListView):
    model = models.Driver


class DriverDetailView(DetailView):
    model = models.Driver


class DriverCreateView(CreateView):
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


class DriverUpdateView(UpdateView):
    model = models.Driver
    form_class = forms.DriverForm

    def get_context_data(self, **kwargs):
        context = super(DriverUpdateView,
                        self).get_context_data(**kwargs)
        context['edit'] = True
        return context
    
    def get_success_url(self):
        return reverse_lazy('sanidad:driver_detail', args=(self.object.pk,))


class DriverDeleteView(View):
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
