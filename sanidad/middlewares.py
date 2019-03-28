from django.utils.deprecation import MiddlewareMixin
from datetime import datetime
from sanidad.models import Inspection
from utils.get_driver_or_company import get_drivers_or_company


class CheckInspectionCompaniesBeat(MiddlewareMixin):

    def process_request(self, request):
        today = datetime.now()
        inspections = Inspection.objects.exclude(
            next_date__year__lte=(today.year - 1))
        today = datetime.strftime(today, "%Y-%m-%d")
        if inspections.count() != 0:
            for inspection in inspections:
                next_date = datetime.strftime(inspection.next_date, "%Y-%m-%d")
                if (str(next_date) <= str(today) and
                 inspection.company_account.is_inspection):
                    data = get_drivers_or_company(inspection.company_account_id)
                    data.is_inspection = False
                    data.save()
