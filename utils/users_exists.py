from django.core.exceptions import ValidationError
from sanidad import models as models_sanidad
from authentication import models as models_authentication


def sanidad_user_exists(document):
    account = models_sanidad.Account.objects.filter(document=document).exists()
    driver = models_sanidad.Driver.objects.filter(document=document).exists()
    return account or driver


def sanidad_company_exists(document):
    return models_sanidad.Company.objects.filter(
        document=document).exists()


def user_exists(document):
    user = models_authentication.User.objects.filter(
        ci=document)
    if user.exists():
        raise ValidationError(
            f'{user.first().get_full_name()} esta como usuario del sistema')
