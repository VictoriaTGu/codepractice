from collections import defaultdict
from copy import deepcopy
from datetime import datetime
from datetime import timedelta
import sys
import json
from heapq import heappush
from heapq import heappop

from classes import DATE_FORMAT
from classes import ScheduledEvent
from income_balancer import IncomeBalancer

START_DATE = '2016-01-01'
AMOUNT_FORMAT = '{0:.2f}'

def main():
    json_dict = json.load(sys.stdin)
    incomes = parse_events(json_dict['incomes'], 'income')
    expenses = parse_events(json_dict['expenses'], 'expense')
    start_date = datetime.strptime(START_DATE, DATE_FORMAT)
    dates_in_year = [start_date + timedelta(days=i) for i in xrange(365)]
    allocations, sources = get_allocations_and_sources(dates_in_year, incomes, expenses)
    income_event_to_spendable_amount = get_smoothed_spendable_income(
        dates_in_year, incomes, allocations
    )
    events = generate_time_series(
        dates_in_year, allocations, sources, incomes, expenses, income_event_to_spendable_amount
    )
    sys.stdout.write(
        json.dumps({"events": events}, indent=4, separators=(',', ': '))
        + '\n'
    )

def parse_events(events, event_type):
    event_lst = []
    for event in events:
        event_lst.append(ScheduledEvent.factory(
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


def get_allocations_and_sources(dates, incomes, expenses):
    available_sources = []
    allocations, sources = defaultdict(list), defaultdict(list)
    start_date = dates[0] if dates else None

    for date in dates:
        for income in incomes:
            amount = income.get_amount_on_date(date)
            if amount is not None:
                seconds_since_start_date = (date - start_date).total_seconds()
                # have to negate the priority keys because heapq only implements min-heap
                heappush(available_sources, (-amount, -seconds_since_start_date, income))

        for expense in expenses:
            amount_owed = expense.get_amount_on_date(date)
            while amount_owed is not None and amount_owed > 0:
                if len(available_sources) == 0:
                    raise_insolvent()
                amount_extracted, income_with_metadata = match_income_source(
                    available_sources, amount_owed, start_date
                )
                # record the income -> expense allocation
                expense_with_metadata = {
                    'date': date, 'event': expense, 'amount_allocated': amount_extracted
                }
                key = (income_with_metadata['date'], income_with_metadata['event'])
                allocations[key].append(expense_with_metadata)
                # record the expense -> income source
                sources[(date, expense)].append(income_with_metadata)

                amount_owed -= amount_extracted

    return allocations, sources


def match_income_source(available_sources, amount_owed, start_date):
    # use the available income source with the largest leftover balance
    (amount_leftover, seconds_since_start_date, income) = heappop(available_sources)
    amount_leftover = abs(amount_leftover)
    amount_extracted = min([amount_leftover, amount_owed])
    amount_leftover -= amount_extracted
    if amount_leftover > 0.0:
        heappush(available_sources, (-amount_leftover, seconds_since_start_date, income))
    income_date = start_date + timedelta(seconds=-seconds_since_start_date)
    income_with_metadata = {
        'date': income_date, 'event': income, 'amount_allocated': amount_extracted
    }
    return amount_extracted, income_with_metadata


def get_smoothed_spendable_income(dates, incomes, allocations):
    if len(dates) == 0:
        return 0.0
    start_date = dates[0]
    balancer = IncomeBalancer(start_date)
    for date in dates:
        for income in incomes:
            if income.get_amount_on_date(date):
                spendable_income = get_spendable_income(date, income, allocations)
                balancer.push(date, spendable_income, income)
    return balancer.to_dict()


def get_spendable_income(date, income, allocations):
    day_spendable_income = 0.0
    amount = income.get_amount_on_date(date)
    if amount is not None:
        day_spendable_income = float(amount) - sum([
            allocation['amount_allocated'] for allocation in allocations[(date, income)]
        ])
    return day_spendable_income


def generate_time_series(dates, allocations, sources, incomes, expenses, income_event_to_spendable_amount):
    events = []
    for date in dates:
        for income in incomes:
            if income.get_amount_on_date(date):
                spendable, amount_to_save = calculate_spendable_and_saved(
                    date, income, allocations, income_event_to_spendable_amount
                )
                events.append(generate_formatted_income_dict(
                    income, date, amount_to_save, spendable, allocations
                ))

        for expense in expenses:
            if expense.get_amount_on_date(date):
                events.append(generate_formatted_expense_dict(
                    expense, date, sources
                ))
    return events


def calculate_spendable_and_saved(date, income, allocations, income_event_to_spendable_amount):
    spendable = get_spendable_income(date, income, allocations)
    spendable_after_smoothing = income_event_to_spendable_amount[(date, income)]
    amount_to_save = max([0.0, spendable - spendable_after_smoothing])
    spendable -= amount_to_save
    return spendable, amount_to_save


def generate_formatted_income_dict(income, date, amount_to_save, spendable, allocations):
    income_event_dict = income.to_dict()
    income_event_dict['date'] = datetime.strftime(date, DATE_FORMAT)
    income_event_dict['saved'] = AMOUNT_FORMAT.format(amount_to_save)
    income_event_dict['spendable'] = AMOUNT_FORMAT.format(spendable)
    income_event_dict['allocations'] = [
        {
            'date': datetime.strftime(allocation['date'], DATE_FORMAT),
            'name': allocation['event'].name,
            'amount': AMOUNT_FORMAT.format(allocation['amount_allocated'])
        }
        for allocation in allocations[(date, income)]
    ]
    return income_event_dict


def generate_formatted_expense_dict(expense, date, sources):
    expense_event_dict = expense.to_dict()
    expense_event_dict['date'] = datetime.strftime(date, DATE_FORMAT)
    expense_event_dict['sources'] = [
        {
            'date': datetime.strftime(source['date'], DATE_FORMAT),
            'name': source['event'].name,
            'amount': AMOUNT_FORMAT.format(source['amount_allocated'])
        }
        for source in sources[(date, expense)]
    ]
    return expense_event_dict


def raise_insolvent():
    sys.stdout.write(json.dumps({"error": 'Insolvent'}) + '\n')
    sys.exit()


if __name__ == "__main__":
    main()
