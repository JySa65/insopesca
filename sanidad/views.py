from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.views.generic import TemplateView, ListView, CreateView, \
    DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from sanidad import models, forms
# Create your views here.


class HomeTemplateView(TemplateView):
    template_name = 'sanidad/home_view.html'


class CompanyListView(ListView):
    model = models.Company

    def get_queryset(self):
        super(CompanyListView, self).get_queryset()
        return self.model.objects.filter(is_delete=False)


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
