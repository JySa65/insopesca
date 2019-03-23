from django.http import Http404
from sanidad.models import Driver, Company

def get_drivers_or_company(pk):
    try:
        data = Driver.objects.get(pk=pk)
        return data
    except Driver.DoesNotExist:
        try:
            data = Company.objects.get(pk=pk)
            return data
        except Company.DoesNotExist:
            raise Http404
