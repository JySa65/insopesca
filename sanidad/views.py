from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.views.generic import TemplateView, ListView, CreateView, \
    DetailView, UpdateView, DeleteView, View
from django.urls import reverse_lazy, reverse
from django.db.models import Q
from utils.check_password import checkPassword
from utils.get_driver_or_company import get_drivers_or_company
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import timedelta, datetime, date
from sanidad import models, forms
from core.models import Notification
from utils.permissions import UserUrlCorrectMixin
from utils.get_data_report import get_company_report, get_type_company_report, \
    get_driver_report, get_inspections_expired
from utils.validate_uuid import validate_uuid4
from uuid import UUID
import json

# Create your views here.


class InspectionDetailApiView(LoginRequiredMixin, View):
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


class InspectionListApiView(LoginRequiredMixin, View):
    model = models.Inspection

    def get(self, *args, **kwargs):
        start = self.request.GET.get('start', '')
        end = self.request.GET.get('end', '')
        queryset = self.model.objects.filter(
            next_date__range=(start, end))
        data = []
        if queryset.count() != 0:
            data = [dict(
                pk=i.pk,
                next_date=i.next_date,
                result=i.result,
                name=i.company_account.get_full_name()
            ) for i in queryset]
        return JsonResponse(data, safe=False)


class HomeTemplateView(LoginRequiredMixin, UserUrlCorrectMixin, TemplateView):
    template_name = 'sanidad/home_view.html'

    def get_context_data(self, **kwargs):
        context = super(HomeTemplateView, self).get_context_data(**kwargs)
        today = datetime.now()
        start = today - timedelta(days=10)
        end = today + timedelta(days=10)
        context['company'] = models.Company.objects.filter(is_inspection=True)
        context['driver'] = models.Driver.objects.filter(is_inspection=True)
        inspection = models.Inspection.objects.filter(
            next_date__range=(start, end), pass_inspection=False)
        inspection_list = []
        for i in inspection:
            if i.company_account.is_inspection:
                inspection_list.append(i)
        context['inspection'] = inspection_list
        context['inspection_expired'] = len(get_inspections_expired())
        years = datetime.now().year
        context['year_list'] = [i for i in range(years - 5, years+1)][::-1]
        return context


class CompanyListView(LoginRequiredMixin, UserUrlCorrectMixin, ListView):
    model = models.Company

    def get_queryset(self):
        super(CompanyListView, self).get_queryset()
        return self.model.objects.filter(is_delete=False)


class TypeCompanyView(LoginRequiredMixin, UserUrlCorrectMixin, View):
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


class CompanyDetailView(LoginRequiredMixin, UserUrlCorrectMixin, DetailView):
    model = models.Company

    def get_object(self):
        pk = self.kwargs.get('pk')
        object = self.model.objects.filter(is_delete=False, pk=pk).first()
        if self.request.user.is_superuser:
            object = get_object_or_404(self.model, pk=pk)
        elif not object:
            raise Http404
        return object


class CompanyCreateView(LoginRequiredMixin, UserUrlCorrectMixin, CreateView):
    model = models.Company
    form_class = forms.CompanyForm

    def get_success_url(self):
        return reverse_lazy('sanidad:company_detail', args=(self.object.pk,))


class CompanyUpdateView(LoginRequiredMixin, UserUrlCorrectMixin, UpdateView):
    model = models.Company
    form_class = forms.CompanyForm

    def get_success_url(self):
        return reverse_lazy('sanidad:company_detail', args=(self.object.pk,))


class CompanyDeleteView(LoginRequiredMixin, UserUrlCorrectMixin, View):
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


class AccoutCompanyCreateView(LoginRequiredMixin, UserUrlCorrectMixin, CreateView):
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
                    account=user.first()
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


class AccoutCompanyDetailView(LoginRequiredMixin, UserUrlCorrectMixin, DetailView):
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


class AccountCompanyUpdateView(LoginRequiredMixin, UserUrlCorrectMixin, UpdateView):
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


class AccountCompanyDeleteView(LoginRequiredMixin, UserUrlCorrectMixin, View):
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


class TransportCompanyCreateView(LoginRequiredMixin, UserUrlCorrectMixin, CreateView):
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


class InspectionCreateView(LoginRequiredMixin, UserUrlCorrectMixin, CreateView):
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
                if (company and not company.is_inspection or
                        driver and not driver.is_inspection):
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
        data = get_drivers_or_company(pk)
        _object = form.save(commit=False)
        _object.company_account = data
        _object.account_register = self.request.user
        data.is_inspection = True

        data.save()
        self.object = _object.save()
        return super(InspectionCreateView, self).form_valid(form)


class InspectionListNotificationView(LoginRequiredMixin, UserUrlCorrectMixin, ListView):
    model = Notification
    template_name = "sanidad/notification_list.html"

    def get_queryset(self):
        super(InspectionListNotificationView, self).get_queryset()
        date = timezone.now()
        start = date - timedelta(days=15)
        end = date + timedelta(days=10)
        return self.model.objects.filter(
            created_at__range=(start, end))


class InspectionListView(LoginRequiredMixin, UserUrlCorrectMixin, ListView):
    model = models.Inspection
    paginate_by = 30


class InspectionDriversCompanyListView(LoginRequiredMixin,
                                       UserUrlCorrectMixin, ListView):

    def get_context_data(self, **kwargs):
        context = super(
            InspectionDriversCompanyListView, self).get_context_data(**kwargs)
        context['type'] = self.kwargs.get("type")
        return context

    def dispatch(self, request, *args, **kwargs):
        if (self.kwargs.get('type')
                not in ['driver', 'company', 'end', 'expired']):
            raise Http404
        return super(
            InspectionDriversCompanyListView, self).dispatch(
                request, *args, **kwargs)

    def get_template_names(self):
        return f'sanidad/{self.kwargs.get("type")}_list_inspection.html'

    def valid_date(self, date1, date2):
        if date1 == "" and date2 == "":
            return False, None, None
        if date1 > date2:
            return False, None, None
        return True, date1, date2

    def get_queryset(self):
        date1 = self.request.GET.get('date1', "")
        date2 = self.request.GET.get('date2', "")
        return dict(
            driver=self.get_drivers,
            company=self.get_companies,
            end=self.get_end,
            expired=self.get_inspections
        )[self.kwargs.get('type')](date1, date2)

    def get_data_query(self, model, date1, date2):
        data_list = []
        status, date1, date2 = self.valid_date(date1, date2)
        datas = model.objects.filter(is_inspection=True)
        for data in datas:
            if status:
                inspection = models.Inspection.objects.filter(
                    company_account_id=data.pk,
                    date__range=(date1, date2)).first()
            else:
                inspection = models.Inspection.objects.filter(
                    company_account_id=data.pk).first()
            if inspection:
                data_list.append(dict(
                    driver=data,
                    inspection=inspection
                ))
        return data_list

    def get_drivers(self, date1, date2):
        return self.get_data_query(
            models.Driver,
            date1, date2)

    def get_companies(self, date1, date2):
        return self.get_data_query(
            models.Company,
            date1, date2)

    def get_end(self, date1, date2):
        today = datetime.now()
        start = today - timedelta(days=10)
        end = today + timedelta(days=10)
        inspection = models.Inspection.objects.filter(
            next_date__range=(start, end), pass_inspection=False)
        inspection_list = []
        for i in inspection:
            if i.company_account.is_inspection:
                inspection_list.append(i)
        return inspection_list
    
    def get_inspections(self, *args):
        return get_inspections_expired()


class InspectionDetailView(LoginRequiredMixin, UserUrlCorrectMixin, DetailView):
    model = models.Inspection


class DriverListView(LoginRequiredMixin, UserUrlCorrectMixin, ListView):
    model = models.Driver


class DriverDetailView(LoginRequiredMixin, UserUrlCorrectMixin, DetailView):
    model = models.Driver


class DriverCreateView(LoginRequiredMixin, UserUrlCorrectMixin, CreateView):
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


class DriverUpdateView(LoginRequiredMixin, UserUrlCorrectMixin, UpdateView):
    model = models.Driver
    form_class = forms.DriverForm

    def get_context_data(self, **kwargs):
        context = super(DriverUpdateView,
                        self).get_context_data(**kwargs)
        context['edit'] = True
        return context

    def get_success_url(self):
        return reverse_lazy('sanidad:driver_detail', args=(self.object.pk,))


class DriverDeleteView(LoginRequiredMixin, UserUrlCorrectMixin, View):
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


class TransportDriverCreateView(LoginRequiredMixin, UserUrlCorrectMixin, CreateView):
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


class ReportGenreralView(LoginRequiredMixin, UserUrlCorrectMixin, TemplateView):
    template_name = "sanidad/view_report.html"

    def get_context_data(self, **kwargs):
        context = super(ReportGenreralView, self).get_context_data(**kwargs)
        type_companys = models.TypeCompany.objects.all()
        companys = models.Company.objects.all()
        driver = models.Driver.objects.all()
        context['type_companys'] = type_companys
        context['companys'] = companys
        context['drivers'] = driver
        years = datetime.now().year
        context['year_list'] = [i for i in range(years - 30, years+1)][::-1]
        return context


class ReportGeneralAPIView(LoginRequiredMixin, UserUrlCorrectMixin, View):

    def get(self, request, *args, **kwargs):
        type_company = request.GET.get('type_company', '')
        company = request.GET.get('company', '')
        driver = request.GET.get('driver', '')
        week1 = request.GET.get('week1', '')
        week2 = request.GET.get('week2', '')
        date = bool(int(request.GET.get('date')))

        if (type_company == "" and company == "" and driver == "" or
                type_company != "" and company != "" and driver != ""):
            data = dict(
                status=False,
                msg="Debes Escoger una compañia o un tipo de compañia"
            )
            return JsonResponse(data)

        if date == 1:
            if week1 == "":
                data = dict(
                    status=False,
                    msg="Asignes Fecha Inicial Para La Consulta"
                )
                return JsonResponse(data)

        if type_company != '':
            data = get_type_company_report(type_company, date, week1, week2)
            return JsonResponse(data, safe=False)

        if company != '':
            data = get_company_report(company, date, week1, week2)
            return JsonResponse(data, safe=False)

        if driver != '':
            data = get_driver_report(driver, date, week1, week2)
            return JsonResponse(data, safe=False)


class ReportInspectionExpired(LoginRequiredMixin, UserUrlCorrectMixin, View):

    def get(self, request, *args, **kwargs):
        data = get_inspections_expired()
        return JsonResponse(data, safe=False)


class UglyReportsView(LoginRequiredMixin, UserUrlCorrectMixin, TemplateView):
    template_name = "sanidad/reports_ugly.html"
    
    def get_context_data(self, **kwargs):
        context = super(
            UglyReportsView, self).get_context_data(**kwargs)
        type_companys = models.TypeCompany.objects.all()
        driver = models.Driver.objects.all()
        companys = models.Company.objects.all()
        
        context['type_companys'] = type_companys
        context['companys'] = companys
        context['driver'] = driver

        context['type'] = self.request.GET.get("type", "")
        documents = self.request.GET.get("document", "")
        date1 = self.request.GET.get('date_range1', "")
        date2 = self.request.GET.get('date_range2', "")
        f_date1, f_date2 = date1.replace("/", ""), date2.replace("/", "")
        print("tp:",context['type'] )
        if len(context['type']) != 1:

            if date1 != "" and date2 != "":

                if (int(f_date1) - int(f_date2) <= 0):

                    start,end = (datetime.strptime((date1+" 0:0"), 
                                "%d/%m/%Y %H:%M").strftime("%Y-%m-%d %H:%M"),
                                    datetime.strptime((date2+" 23:59"), 
                                        "%d/%m/%Y %H:%M").strftime("%Y-%m-%d %H:%M"))

                    if context['type'] =="all_company":

                        context['all_company'] = models.Company.objects.filter(created_at__range=(start, end))

                    elif context['type'] == "all_driver":

                        context['all_driver'] = models.Driver.objects.filter(
                            created_at__range=(start, end))
                    else:
                        print("asdasdasds")
                        context['msg'] = "Esta Haciendo Algo Raro :'c"

                else:
                    context['msg'] = "RANGO DE FECHA INCORRECTO."
           
            else:
                if context['type'] =="individual_company":
                    if len(documents) != 0:
                        if not (validate_uuid4(documents)):
                            context['msg'] = "Esta Haciendo Algo Raro :'c"
                        
                        else:
                            context['individual_company'] = models.Company.objects.filter(pk=documents)
                            if len(context['individual_company']) == 0:
                                context['msg'] = "No se encontraron Coincidencias."
                    else:
                        context['msg'] = "Falta el Documento."

                elif context['type'] =="individual_driver":
                    if len(documents)  != 0:
                        if not (validate_uuid4(documents)):
                            context['msg'] = "Esta Haciendo Algo Raro :'c"
                        else:
                            context['individual_driver'] = models.Driver.objects.filter(pk=documents)
                    else:
                        context['msg'] = "Falta el Documento."

                elif context['type'] == "all_company":
                    context['all_company'] = models.Company.objects.all()

                elif context['type'] == "all_driver":
                    context['all_driver'] = models.Driver.objects.all()
                else:
                    context['msg'] = "Esta Haciendo Algo Raro :'c"                    
        else:
            context['msg'] = "No Pasaras La Seguridad del Sistema."

        return context


class HomeGrapichView(TemplateView):
    template_name = 'sanidad/home_grapich.html'

    def get_context_data(self, **kwargs):
        context = super(HomeGrapichView, self).get_context_data(**kwargs)
        years = datetime.now().year
        context['year_list'] = [i for i in range(years - 5, years+1)][::-1]
        return context
