from datetime import datetime
from datetime import timedelta
import sys
import json
from Queue import LifoQueue

from classes import DATE_FORMAT
from classes import AccountingEvent

START_DATE = '2016-01-01'

def main():
    json_dict = json.load(sys.stdin)
    income_lst = parse_events(json_dict['incomes'])
    expense_lst = parse_events(json_dict['expenses'])
    get_time_series(expense_lst)

def parse_events(events):
    event_lst = []
    for event in events:
        event_lst.append(AccountingEvent.factory(
            common_attr={
                'name': event.get('name'),
                'amount': event.get('amount', 0),
                'start_date': event.get('schedule', {}).get('start', START_DATE),
            },
            event_type=event['schedule']['type'],
            addl_info=event['schedule']
        ))
    return event_lst


def get_time_series(event_lst):
    stack = LifoQueue()
    base = datetime.strptime(START_DATE, DATE_FORMAT)
    dates_in_year = [base + timedelta(days=i) for i in xrange(365)]
    for date in dates_in_year:
        for event in event_lst:
            if event.get_amount_on_date(date):
                stack.put(event)
                print date, str(event)



if __name__ == "__main__":
    main()
