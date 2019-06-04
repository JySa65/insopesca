from django.utils.deprecation import MiddlewareMixin
from datetime import datetime
from sanidad.models import Inspection
from utils.get_driver_or_company import get_drivers_or_company
import asyncio


class CheckInspectionCompaniesBeat(MiddlewareMixin):

    def process_request(self, request):
        if (request.user.level == 'is_sanid' or 
            request.user.is_superuser or request.user.role == 'is_coordinator'):
            self.check_inspections
        # loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(loop)
        # loop.run_in_executor(None, )

    def check_inspections(self):
        today = datetime.now()
        inspections = Inspection.objects.exclude(
            next_date__year__lte=(today.year - 2)).filter(pass_inspection=False)
        today = datetime.strftime(today, "%Y-%m-%d")
        if inspections.count() != 0:
            for inspection in inspections:
                next_date = datetime.strftime(inspection.next_date, "%Y-%m-%d")
                if (str(next_date) <= str(today)):
                    data = get_drivers_or_company(
                        inspection.company_account_id)
                    data.is_inspection = False
                    data.save()
                    inspection.pass_inspection = True
                    inspection.save()
