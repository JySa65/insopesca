from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
# generic View
from django.views.generic import CreateView, ListView, UpdateView, \
    DeleteView, DetailView, FormView, TemplateView, View
# serializer
from django.core import serializers
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
import json
# Create your views here.


class UserListView(LoginRequiredMixin, ListView):
    model = models.User

    def get_queryset(self):
        super(UserListView, self).get_queryset()
        return self.model.objects.filter(is_delete=False, is_superuser=False).exclude(
            email=self.request.user.email
        )


class UserDetailView(LoginRequiredMixin, DetailView):
    model = models.User

    def get_context_data(self, *args, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        context['questions'] = models.SecurityQuestion.objects.filter(
            user__pk=self.request.user.pk)
        return context


class UserCreateView(LoginRequiredMixin, CreateView):
    model = models.User
    form_class = forms.UserCreateForm

    def form_valid(self, form):
        _object = form.save(commit=False)
        _object.set_password(_object.ci)
        self.object = _object.save()
        return super(UserCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('authentication:detail', args=(self.object.pk,))


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = models.User
    form_class = forms.UserUpdateForm
    success_url = reverse_lazy('authentication:list')


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = models.User
    success_url = reverse_lazy('authentication:list')


class UserAdminDetailView(LoginRequiredMixin, DetailView):
    model = models.User

    def get_object(self):
        user = self.request.user.pk
        object = get_object_or_404(self.model, pk=user)
        return object

    def get_context_data(self, **kwargs):
        context = super(UserAdminDetailView,
                        self).get_context_data(**kwargs)
        context['questions'] = models.SecurityQuestion.objects.filter(
            user__pk=self.request.user.pk)
        context['profile'] = True
        return context


class UserAdminUpdateView(LoginRequiredMixin, UpdateView):
    model = models.User
    form_class = forms.UserUpdateForm

    def get_object(self):
        user = self.request.user.pk
        object = get_object_or_404(self.model, pk=user)
        return object

    def get_context_data(self, **kwargs):
        context = super(UserAdminUpdateView,
                        self).get_context_data(**kwargs)
        context['profile'] = True
        return context

    def form_valid(self, form):
        _object = form.save(commit=False)
        _object.is_active = True
        self.object = _object.save()
        return super(UserAdminUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('authentication:detail_profile')


class SecurityQuestionCreateView(LoginRequiredMixin, FormView):
    model = models.SecurityQuestion
    form_class = forms.SecurityQuestionForm
    template_name = 'authentication/securityquestion_form.html'

    def get_context_data(self, **kwargs):
        context = super(SecurityQuestionCreateView,
                        self).get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

    def post(self, *args, **kwargs):
        form = self.form_class(self.request.POST)
        if form.is_valid():
            self.model.objects.filter(user=self.request.user).delete()
            user = get_object_or_404(models.User, pk=self.request.user.pk)
            question_one = form.cleaned_data.get("question_one")
            question_two = form.cleaned_data.get("question_two")
            question_three = form.cleaned_data.get("question_three")
            answer_one = form.cleaned_data.get("answer_one")
            answer_two = form.cleaned_data.get("answer_two")
            answer_three = form.cleaned_data.get("answer_three")
            securitys = [
                {'question': question_one, 'answer': answer_one},
                {'question': question_two, 'answer': answer_two},
                {'question': question_three, 'answer': answer_three}
            ]
            for security in securitys:
                self.model.objects.create(**security, user=user)
            user.question = True
            user.save()
            return HttpResponseRedirect(
                reverse_lazy(
                    'authentication:detail', args=(self.kwargs['pk'],)))
        return render(self.request, self.template_name, {'form': form})


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


class RestoreDataUser(LoginRequiredMixin, View):
    model = models.User

    def post(self, request, *args, **kwargs):
        try:
            pk = int(json.loads(str(request.body, 'utf-8')).get('pk'))
            user = get_object_or_404(self.model, pk=pk)
            user.set_password(user.ci)
            user.change_pass = False
            user.save()
            data = {
                "status": True,
            }
            return JsonResponse(data, safe=False)
        except Exception as e:
            data = {
                "status": False,
                "msg": e
            }
            return JsonResponse(data, safe=False)
        

class ForgotPassword(FormView):
    model = models.SecurityQuestion
    template_name = "authentication/forgot_password.html"