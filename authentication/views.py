from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
# generic View
from django.views.generic import CreateView, ListView, UpdateView, \
    DeleteView, DetailView, FormView, TemplateView
# login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
# reverse lazy
from django.urls import reverse_lazy
# login Required
from django.contrib.auth.mixins import LoginRequiredMixin
# change password
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
# Model Authentication
from authentication import models, forms
# Create your views here.


class UserListView(LoginRequiredMixin, ListView):
    model = models.User

    def get_queryset(self):
        super(UserListView, self).get_queryset()
        return self.model.objects.filter(is_delete=False)


class UserDetailView(LoginRequiredMixin, DetailView):
    model = models.User


class UserCreateView(LoginRequiredMixin, CreateView):
    model = models.User
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('authentication:list')


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = models.User
    form_class = forms.UserUpdateForm
    success_url = reverse_lazy('authentication:list')


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = models.User
    success_url = reverse_lazy('authentication:list')

class HomePageFormView(TemplateView):
    template_name = "authentication/homepage.html"


class LoginFormView(FormView):
    form_class = AuthenticationForm
    template_name = "authentication/login.html"

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(email=username, password=password)
        if user is not None:
            login(request, user)
            url_next = request.GET.get('next')
            if url_next is not None:
                return HttpResponseRedirect(url_next)
            else:
                return HttpResponseRedirect(reverse_lazy("authentication:list"))
        else:
            msg = "Usuario o Contraseña Incorrecta"
            return render(request, self.template_name, {'form': self.form_class, 'message': msg})

        return render(request, self.template_name, {'form': self.form_class})


class ChangePassword(LoginRequiredMixin, FormView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy("login")
    template_name = 'authentication/change_password.html'

    def get_form_kwargs(self):
        kwargs = super(ChangePassword, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        _object = form.save(commit=False)
        _object.change_pass = True
        user = _object.save()
        update_session_auth_hash(self.request, user)
        logout(self.request)
        return super(ChangePassword, self).form_valid(form)
