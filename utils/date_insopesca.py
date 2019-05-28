import datetime


class DateInsopesca():

    def __init__(self, p_year, p_week, *args, **kwargs):
        self.p_year = p_year
        self.p_week = p_week

    def get_date_first_week(self):
        return datetime.datetime.strptime(
            f'{self.p_year}-W{int(self.p_week)-1}-1', "%Y-W%W-%w").date()

    def get_date_range_from_week(self):
        firstdayofweek = self.get_date_first_week()
        lastdayofweek = firstdayofweek + datetime.timedelta(days=6.9)
        return firstdayofweek, lastdayofweek

    def get_month_from_week_number(self):
        date = self.get_date_first_week()
        return date.month
