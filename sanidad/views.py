from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.views.generic import TemplateView, ListView, CreateView, \
    DetailView, UpdateView, DeleteView, View
from django.urls import reverse_lazy, reverse
from utils.check_password import checkPassword
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
                    id=save_name.pk,
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


class CompanyDeleteView(DeleteView):
    model = models.Company

    def post(self, *args, **kwargs):
        company = self.get_object()
        company.is_delete = True
        company.is_active = False
        company.save()
        return HttpResponseRedirect(reverse_lazy('sanidad:company_list'))


class AccoutCompanyCreateView(CreateView):
    model = models.Account
    form_class = forms.AccountForm
    template_name = 'sanidad/account_form.html'

    def get_object(self):
        return get_object_or_404(models.Company, pk=self.kwargs.get('pk'))

    def get_context_data(self, *args, **kwargs):
        context = super(AccoutCompanyCreateView,
                        self).get_context_data(**kwargs)
        company = self.get_object()
        context['company'] = company
        search = self.request.GET.get('search', '')
        if search != '':
            user = self.model.objects.filter(document=search).first()
            if user:
                user_exists = models.CompanyHasAccount.objects.filter(
                    account=user).exists()
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
                user_exists = company.account.all().filter(pk=user.pk).exists()
                if not user_exists:
                    company.account.add(user)
                    return HttpResponseRedirect(
                        reverse_lazy('sanidad:company_detail', args=(company.pk,)))
            except self.model.DoesNotExist:
                return HttpResponseRedirect(
                    reverse_lazy('sanidad:company_detail', args=(company.pk,)))
        user = self.model.objects.filter(document=ci)
        if user.exists():
            user_exists = company.account.all().filter(pk=user.first().pk).exists()
            if not user_exists:
                company.account.add(user.first())
                return HttpResponseRedirect(
                    reverse_lazy('sanidad:company_detail', args=(company.pk,)))
            return render(self.request, self.template_name, {
                'form': form, 'company': company})

        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            company.account.add(user)
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
        context['company'] = self.object.company_set.all().filter(
            pk=self.kwargs.get('pk')).first()
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
        return self.object.company_set.all().filter(
            pk=self.kwargs.get('pk')).first()


class AccountCompanyDeleteView(DeleteView):
    model = models.Company
    # pk_url_kwarg = 'account'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        account = get_object_or_404(
            models.Account, pk=self.kwargs.get('account'))
        self.object.account.remove(account)
        self.object.save()
        return HttpResponseRedirect(
            reverse_lazy('sanidad:company_detail', args=(self.kwargs.get('pk'),)))


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
        return context

    def form_valid(self, form):
        _object = form.save(commit=False)
        _object.type = f'is_{self.kwargs.get("type")}'
        self.object = _object.save()
        return super(TransportCompanyCreateView, self).form_valid(form)

    def get_form(self, form_class=None):
        form_class = forms.TransportLandForm
        if self.kwargs.get("type") != 'land':
            form_class = forms.TransportMaritimeForm
        return form_class(**self.get_form_kwargs())

    def get_success_url(self):
        self.object.company.add(self.get_object())
        return reverse_lazy('sanidad:company_detail', args=(
            self.kwargs.get('pk'),))
