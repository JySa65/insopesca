from sanidad import models as models_sanidad


def sanidad_user_exists(document):
    account = models_sanidad.Account.objects.filter(document=document).exists()
    driver = models_sanidad.Driver.objects.filter(document=document).exists()
    return account or driver


def sanidad_company_exists(document):
    return models_sanidad.Company.objects.filter(
        document=document).exists()
