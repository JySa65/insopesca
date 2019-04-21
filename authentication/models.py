from django.db import models
from django.contrib.auth.models import AbstractBaseUser, \
    PermissionsMixin, BaseUserManager
from django.utils.translation import ugettext, ugettext_lazy as _
from django.utils import timezone
from simple_history.models import HistoricalRecords
from utils.Select import Selects
import datetime
# Create your models here.


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError(_('User must have a valid email address.'))
        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.create_user(email, password, **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    ci = models.CharField(_('Cedula'), max_length=8, blank=False, null=False, unique=True)
    name = models.CharField(_('Nombres'), max_length=50,
                            blank=False, null=False)
    last_name = models.CharField(_('Apellidos'), max_length=50,
                                 blank=False, null=False)
    email = models.EmailField(_('Correo Electronico'), null=False,
                              blank=False, unique=True)

    # user
    uuid = models.CharField(_("Uuid"), max_length=50, null=True, blank=True)
    change_pass = models.BooleanField(_("Cambio La Contraseña"), default=False)
    question = models.BooleanField(_("Completo Sus Preguntas"), default=False)
    is_active = models.BooleanField(_('Es Activo'), default=True)
    is_staff = models.BooleanField(_('Es Staff'), default=False)
    is_superuser = models.BooleanField(
        _('Es Super Usuario'), default=False)
    is_delete = models.BooleanField(_('Eliminado'), default=False)
    ip = models.CharField(_('Direccion IP'), max_length=20)
    role = models.CharField(_('Rol'), max_length=500,
                            null=True, blank=True, choices=Selects().role())
    level = models.CharField(_('Level'), max_length=50,
                             null=True, blank=True, choices=Selects().level())
    # join
    date_joined = models.DateTimeField(
        _('Unido Desde'), default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()
    objects = UserManager()
    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = "User"
        ordering = ('-created_at',)

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f'{self.name} {self.last_name}'

    def get_short_name(self):
        return self.name


class SecurityQuestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.TextField(_("Pregunta"), null=False)
    answer = models.TextField(_("Respuesta"), null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords(user_model=User)
    
    class Meta:
        verbose_name = "Pregunta De Seguridad"
        verbose_name_plural = "Preguntas De Seguridad"
        ordering = ('-created_at',)

    def __str__(self):
        return self.user.email

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value
