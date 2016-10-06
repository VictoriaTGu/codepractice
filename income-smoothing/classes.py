from datetime import datetime

DATE_FORMAT = '%Y-%m-%d'


class AccountingEvent(object):
    # factory for generating the different types of incomes and expenses
    def factory(common_attr, event_type, addl_info=None):
        if event_type == "interval":
            return IntervalEvent(common_attr=common_attr, period=addl_info['period'])
        elif event_type == "monthly":
            return MonthlyEvent(common_attr=common_attr, days=addl_info['days'])
        elif event_type == "oneTime":
            return OneTimeEvent(common_attr=common_attr)
        else:
            raise ValueError
    factory = staticmethod(factory)

    def get_amount_on_date(self, date):
        raise NotImplementedError

class MonthlyEvent(AccountingEvent):
    def __init__(self, common_attr, days):
        self.name = common_attr['name']
        self.amount = common_attr['amount']
        self.start_date = datetime.strptime(common_attr['start_date'], DATE_FORMAT)
        self.days = days

    def __str__(self):
        return ' '.join([
            'Monthly', self.name, str(self.amount),
            datetime.strftime(self.start_date, DATE_FORMAT), str(self.days)
        ])

    def get_amount_on_date(self, current_date):
        if current_date.day in self.days:
            return self.amount

class IntervalEvent(AccountingEvent):
    def __init__(self, common_attr, period):
        self.name = common_attr['name']
        self.amount = common_attr['amount']
        self.start_date = datetime.strptime(common_attr['start_date'], DATE_FORMAT)
        self.period = period

    def __str__(self):
        return ' '.join([
            'Interval', self.name, str(self.amount),
            datetime.strftime(self.start_date, DATE_FORMAT), str(self.period)
        ])

    def get_amount_on_date(self, current_date):
        timedelta = current_date - self.start_date
        if timedelta.days >= 0 and timedelta.days % self.period == 0:
            return self.amount

class OneTimeEvent(AccountingEvent):
    def __init__(self, common_attr):
        self.name = common_attr['name']
        self.amount = common_attr['amount']
        self.start_date = datetime.strptime(common_attr['start_date'], DATE_FORMAT)

    def __str__(self):
        return ' '.join([
            'OneTime', self.name, str(self.amount),
            datetime.strftime(self.start_date, DATE_FORMAT)
        ])

    def get_amount_on_date(self, current_date):
        if self.start_date.date() == current_date.date():
            return self.amount
