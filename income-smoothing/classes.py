"""Classes that implement get_amount_on_date(date) for different schedules of
incomes and expenses and a base class that exposes a factory method for
generating the appropriate class instances.

Usage:
    ScheduledEvent.factory(
        common_attr={
            'name': 'SomeName',
            'amount': 100,
            'start_date': datetime.datetime(2016,1,1),
            event_type: income
        },
        event_frequency='monthly',
        addl_info={}
    )
"""
from datetime import datetime

DATE_FORMAT = '%Y-%m-%d'


class ScheduledEvent(object):
    def factory(common_attr, event_frequency, addl_info=None):
        if event_frequency == "interval":
            return IntervalEvent(common_attr=common_attr, period=addl_info['period'])
        elif event_frequency == "monthly":
            return MonthlyEvent(common_attr=common_attr, days=addl_info['days'])
        elif event_frequency == "oneTime":
            return OneTimeEvent(common_attr=common_attr)
        else:
            raise ValueError
    factory = staticmethod(factory)

    def get_amount_on_date(self, date):
        raise NotImplementedError

    def __str__(self):
        return ' '.join([
            self.name, str(self.amount),
            datetime.strftime(self.start_date, DATE_FORMAT)
        ])

    def __init__(self, common_attr):
        self.name = common_attr['name']
        self.amount = common_attr['amount']
        self.start_date = datetime.strptime(common_attr['start_date'], DATE_FORMAT)
        self.event_type = common_attr['event_type']

    def __eq__(self, other_event):
        if self.name != other_event.name:
            return False
        if self.amount != other_event.amount:
            return False
        if self.start_date != other_event.start_date:
            return False
        if self.event_type != other_event.event_type:
            return False
        return True

    def to_dict(self):
        return {'type': self.event_type, 'name': self.name}


class MonthlyEvent(ScheduledEvent):
    def __init__(self, common_attr, days):
        super(MonthlyEvent, self).__init__(common_attr)
        self.days = days
        self.leftover_amount = self.amount

    def __str__(self):
        return ' '.join([
            'Monthly', super(MonthlyEvent, self).__str__(), str(self.days)
        ])

    def get_amount_on_date(self, current_date):
        if current_date.day in self.days:
            return self.amount


class IntervalEvent(ScheduledEvent):
    def __init__(self, common_attr, period):
        super(IntervalEvent, self).__init__(common_attr)
        self.period = period

    def __str__(self):
        return ' '.join([
            'Interval', super(IntervalEvent, self).__str__(), str(self.period)
        ])

    def get_amount_on_date(self, current_date):
        timedelta = current_date - self.start_date
        if timedelta.days >= 0 and timedelta.days % self.period == 0:
            return self.amount


class OneTimeEvent(ScheduledEvent):
    def __init__(self, common_attr):
        super(OneTimeEvent, self).__init__(common_attr)

    def __str__(self):
        return ' '.join([
            'OneTime', super(OneTimeEvent, self).__str__()
        ])

    def get_amount_on_date(self, current_date):
        if self.start_date.date() == current_date.date():
            return self.amount
