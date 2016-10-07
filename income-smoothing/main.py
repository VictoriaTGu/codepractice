from collections import defaultdict
from copy import deepcopy
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
    incomes = parse_events(json_dict['incomes'], 'income')
    expenses = parse_events(json_dict['expenses'], 'expense')
    base = datetime.strptime(START_DATE, DATE_FORMAT)
    dates_in_year = [base + timedelta(days=i) for i in xrange(365)]
    allocations, sources = get_allocations_and_sources(incomes, expenses, dates_in_year)
    events = generate_time_series(dates_in_year, allocations, sources, incomes, expenses)
    sys.stdout.write(
            json.dumps({"events": events}, sort_keys=True, indent=4, separators=(',', ': '))
            + '\n'
    )

def parse_events(events, event_type):
    event_lst = []
    for event in events:
        event_lst.append(AccountingEvent.factory(
            common_attr={
                'name': event.get('name'),
                'amount': event.get('amount', 0),
                'start_date': event.get('schedule', {}).get('start', START_DATE),
                'event_type': event_type,
            },
            event_frequency=event['schedule']['type'],
            addl_info=event['schedule']
        ))
    return event_lst


def get_allocations_and_sources(incomes, expenses, dates):
    available_sources = LifoQueue()
    allocations, sources = defaultdict(list), defaultdict(list)
    for date in dates:
        for income in incomes:
            amount = income.get_amount_on_date(date)
            if amount is not None:
                income_with_metadata = {
                        'date': date, 'event': income, 'amount_leftover': amount
                }
                available_sources.put(income_with_metadata)
        for expense in expenses:
            amount_owed = expense.get_amount_on_date(date)
            while amount_owed is not None and amount_owed > 0:
                if available_sources.empty():
                    raise_insolvent()

                income_with_metadata = available_sources.get()
                amount_extracted = min([income_with_metadata['amount_leftover'], amount_owed])
                income_with_metadata['amount_leftover'] -= amount_extracted
                if income_with_metadata['amount_leftover'] > 0.0:
                    available_sources.put(income_with_metadata)

                expense_with_metadata = {
                        'date': date, 'event': expense, 'amount': amount_extracted
                }
                allocations[
                    (income_with_metadata['date'], income_with_metadata['event'])
                ].append(expense_with_metadata)
                income_copy = deepcopy(income_with_metadata)
                income_copy['amount_allocated'] = amount_extracted
                sources[(date, expense)].append(income_copy)

                amount_owed -= amount_extracted

    return allocations, sources

def generate_time_series(dates, allocations, sources, incomes, expenses):
    events = []
    for date in dates:
        for income in incomes:
            if income.get_amount_on_date(date):
                income_event_dict = income.to_dict()
                income_event_dict['date'] = datetime.strftime(date, DATE_FORMAT)
                income_event_dict['allocations'] = [
                    {
                        'date': datetime.strftime(allocation['date'], DATE_FORMAT),
                        'name': allocation['event'].name,
                        'amount': allocation['amount']
                    }
                    for allocation in allocations[(date, income)]
                ]
                events.append(income_event_dict)

        for expense in expenses:
            if expense.get_amount_on_date(date):
                expense_event_dict = expense.to_dict()
                expense_event_dict['date'] = datetime.strftime(date, DATE_FORMAT)
                expense_event_dict['sources'] = [
                    {
                        'date': datetime.strftime(source['date'], DATE_FORMAT),
                        'name': source['event'].name,
                        'amount': source['amount_allocated']
                    }
                    for source in sources[(date, expense)]
                ]
                events.append(expense_event_dict)
    return events


def raise_insolvent():
    sys.stdout.write(json.dumps({"error": 'Insolvent'}) + '\n')
    sys.exit()


if __name__ == "__main__":
    main()
