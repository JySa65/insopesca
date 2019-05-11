from django.contrib.sessions.models import Session
from django.db.models import Q
from django.db import transaction
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
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
from utils.Select import Selects
from utils.permissions import AdminRequiredMixin
from django.contrib import messages
import asyncio
from utils.back_restore_db import BackupRestoreDBConfig

# Create your views here.

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


class UserDetailApiView(LoginRequiredMixin, AdminRequiredMixin, View):
    model = models.User

    def get(self, request, *args, **kwargs):
        data = request.GET.get('data', '')
        if data != '':
            user = self.model.objects.filter(
                Q(ci=data) | Q(email=data)).exclude(pk=request.user.pk).first()
            if user:
                data = dict(
                    status=True,
                    user=dict(
                        pk=user.pk,
                        document=user.ci,
                        name=user.get_full_name(),
                        is_active=user.is_active,
                        is_delete=user.is_delete
                    )
                )
                return JsonResponse(data)
        return JsonResponse(dict(status=False))


class UserListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = models.User

    def get_queryset(self):
        super(UserListView, self).get_queryset()
        # data = dict(self.request.GET)
        # self.model.objects.filter(**data)
        return self.model.objects.filter(is_delete=False, is_superuser=False).exclude(
            email=self.request.user.email
        )


class UserDetailView(LoginRequiredMixin, AdminRequiredMixin, DetailView):
    model = models.User

    def get_context_data(self, *args, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        context['questions'] = models.SecurityQuestion.objects.filter(
            user__pk=self.request.user.pk)
        return context


class UserCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = models.User
    form_class = forms.UserCreateForm

    def form_valid(self, form):
        _object = form.save(commit=False)
        _object.set_password(_object.ci)
        self.object = _object.save()
        return super(UserCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('authentication:detail', args=(self.object.pk,))


class UserUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = models.User
    form_class = forms.UserUpdateForm
    success_url = reverse_lazy('authentication:list')

    def form_valid(self, form):
        _object = form.save(commit=False)
        _type = self.request.GET.get('type')
        if _type == 'delete':
            _object.is_delete = False
        if _type == 'active':
            _object.is_active = True
        self.object = _object.save()
        return super(UserUpdateView, self).form_valid(form)


class UserDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = models.User

    def post(self, *args, **kwargs):
        user = self.get_object()
        user.is_delete = True
        user.is_active = False
        user.change_pass = False
        user.set_password(user.ci)
        user.save()
        return HttpResponseRedirect(reverse_lazy('authentication:list'))


class UserAdminDetailView(LoginRequiredMixin, AdminRequiredMixin, DetailView):
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


class UserAdminUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
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
            with transaction.atomic():
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
                if self.request.user.is_superuser or self.request.user.role == 'is_coordinator':
                    return HttpResponseRedirect(
                        Selects().level_user_url()['is_admin_or_coordinator'])
                else:
                    return HttpResponseRedirect(Selects().level_user_url()[user.level])
        return render(self.request, self.template_name, {'form': form})


class LoginFormView(FormView):
    form_class = AuthenticationForm
    template_name = "authentication/login.html"

    def render_user(self, user):
        if user.is_superuser or user.role == 'is_coordinator':
            return HttpResponseRedirect(Selects().level_user_url()['is_admin_or_coordinator'])
        else:
            return HttpResponseRedirect(Selects().level_user_url()[user.level])

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return self.render_user(request.user)
        return super(LoginFormView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(email=username, password=password)
        if user is not None:
            login(request, user)
            session = Session.objects.get(
                session_key=request.session.session_key)
            user_session = models.SessionUser.objects.filter(user=user).first()
            try:
                with transaction.atomic():
                    models.SessionUser.objects.create(
                        user=user, session=session)
                self.fail('Duplicate Session')
            except Exception:
                if user_session:
                    with transaction.atomic():
                        Session.objects.get(
                            session_key=user_session.session.session_key).delete()
                        models.SessionUser.objects.create(
                            user=user, session=session)
            url_next = request.GET.get('next')
            if url_next is not None:
                return HttpResponseRedirect(url_next)
            else:
                return self.render_user(user)
        msg = "Usuario o Contraseña Incorrecta"
        messages.add_message(self.request, messages.INFO, msg)
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
        messages.add_message(self.request,
                             messages.INFO,
                             'Contraseña Cambiada Exitosamente')
        update_session_auth_hash(self.request, user)
        logout(self.request)
        return super(ChangePassword, self).form_valid(form)


@method_decorator(csrf_exempt, name='dispatch')
class RestoreDataUser(LoginRequiredMixin, View):
    model = models.User

    def post(self, request, *args, **kwargs):
        try:
            pk = int(json.loads(str(request.body, 'utf-8')).get('pk'))
            user = get_object_or_404(self.model, pk=pk)
            user.set_password(user.ci)
            user.change_pass = False
            user.is_active = True
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


@method_decorator(csrf_exempt, name='dispatch')
class ForgotPassword(FormView):
    model = models.User
    template_name = "authentication/forgot_password.html"
    form_class = forms.ForgotPasswordForm

    def post(self, request, *args, **kwargs):
        try:
            email = json.loads(str(request.body, 'utf-8')).get('email')
        except Exception:
            data = {
                "status": False,
                "msg": "Correo Electronico Requerido"
            }
            return JsonResponse(data)

        try:
            user = self.model.objects.get(email=email)
            questions = models.SecurityQuestion.objects.filter(user=user)
            user.is_active = False
            user.save()

            if len(questions) == 0:
                data = {
                    "status": False,
                    "msg": f"Usuario: {user.email} No Tiene Pregunta Registrada. Por Favor Comuniquese Con El Administrador del Sistema"
                }
                return JsonResponse(data)

            data = {
                'status': True,
                'data': {
                    'email': user.email,
                    'questions': []
                }
            }
            for question in questions:
                data['data']['questions'].append({
                    'id': question.pk,
                    'question': question.question
                })
            return JsonResponse(data)
        except self.model.DoesNotExist:
            return JsonResponse({
                'status': False,
                'msg': 'Correo Electronico Incorrecto'
            })

    def put(self, request, *args, **kwargs):
        data = json.loads(str(request.body, 'utf-8'))
        email = data.get('email')
        answers = data.get('answers')
        if email == "":
            return JsonResponse({
                'status': False,
                'msg': 'Correo Electronico Requerido'
            })
        try:
            user = self.model.objects.get(email=email)
        except self.model.DoesNotExist:
            return JsonResponse({
                'status': False,
                'msg': 'Usuario No Existe'
            })

        for answer in answers:
            id = answer.get('id')
            ans = answer.get('answer')
            if id == "" or ans == "":
                return JsonResponse({
                    'status': False,
                    'msg': 'Faltaron Algunas Respuestas'
                })
            answ = models.SecurityQuestion.objects.filter(
                pk=id, user=user).first()
            if answ.answer != ans:
                data = {
                    "status": False,
                    "msg": f"Algunas Preguntas Tienen Una Respuesta Invalida"
                }
                return JsonResponse(data)

        user.set_password(user.ci)
        user.is_active = True
        user.change_pass = False
        user.save()
        return JsonResponse({
            'status': True,
            'msg': 'Clave Reestablecida Exitosamente Es Su Cedula Recuerde Cambiarla'
        })


class BackupBDView(LoginRequiredMixin, TemplateView):
    template_name = "authentication/bd.html"

    def post(self, request, *args, **kwargs):
        bd = BackupRestoreDBConfig()
        loop.run_in_executor(None, bd.back_up, request.user)
        data = dict(
            status=True,
            msg="Le Avisaremos Cuando Este Listo"
        )
        return JsonResponse(data)


class BackupBDAPiView(LoginRequiredMixin, View):
    model = models.BackupRestoreBD

    def get(self, request, *args, **kwargs):
        data = self.model.objects.select_related(
            'user').all().order_by('-created_at')
        serialize = json.loads(
            serializers.serialize(
                'json', data, fields=('created_at', 'user')))
        return JsonResponse(serialize, safe=False)

    def post(self, request, *args, **kwargs):
        try:
            bd = BackupRestoreDBConfig()
            pk = int(json.loads(str(request.body, 'utf-8')).get('id'))
            model = get_object_or_404(self.model, pk=pk)
            loop.run_in_executor(None, bd.restore, model.pk)
            data = dict(
                status=True,
                msg="Espere Por Favor"
            )
            return JsonResponse(data)
        except Exception as e:
            data = dict(
                status=False,
                msg=e
            )
            return JsonResponse(data)
