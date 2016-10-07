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
    base = datetime.strptime(START_DATE, DATE_FORMAT)
    dates_in_year = [base + timedelta(days=i) for i in xrange(365)]
    allocations, sources = get_allocations_and_sources(incomes, expenses, dates_in_year)
    income_event_to_spendable_amount = get_smoothed_spendable_income(dates_in_year, incomes, allocations)
    events = generate_time_series(dates_in_year, allocations, sources, incomes, expenses, income_event_to_spendable_amount)
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


def get_allocations_and_sources(incomes, expenses, dates):
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

                # use the available income source with the largest leftover balance
                (amount_leftover, seconds_since_start_date, income) = heappop(available_sources)
                amount_leftover = abs(amount_leftover)
                amount_extracted = min([amount_leftover, amount_owed])
                amount_leftover -= amount_extracted
                if amount_leftover > 0.0:
                    heappush(available_sources, (-amount_leftover, seconds_since_start_date, income))

                expense_with_metadata = {
                    'date': date, 'event': expense, 'amount_allocated': amount_extracted
                }
                # record the income -> expense allocation
                income_date = start_date + timedelta(seconds=-seconds_since_start_date)
                allocations[(income_date, income)].append(expense_with_metadata)
                # record the expense -> income source
                income_with_metadata = {
                    'date': income_date, 'event': income, 'amount_allocated': amount_extracted
                }
                sources[(date, expense)].append(income_with_metadata)

                amount_owed -= amount_extracted

    return allocations, sources


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
    saved = 0.0
    for date in dates:
        for income in incomes:
            if income.get_amount_on_date(date):
                spendable = get_spendable_income(date, income, allocations)
                spendable_after_smoothing = income_event_to_spendable_amount[(date, income)]

                amount_to_save = max([0.0, spendable - spendable_after_smoothing])
                spendable -= amount_to_save
                # print 'savings balance:', saved, 'spending:', spendable, 'amount saved:', amount_to_save
                if spendable < spendable_after_smoothing:
                    taking_from_savings = min(saved, spendable_after_smoothing - spendable)
                    # print 'taking from savings:', taking_from_savings, '=', spendable + taking_from_savings
                    saved -= taking_from_savings
                    print 'taking from savings', spendable + taking_from_savings
                else:
                    print 'spending', spendable
                saved += amount_to_save

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
                events.append(income_event_dict)

        for expense in expenses:
            if expense.get_amount_on_date(date):
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
                events.append(expense_event_dict)
    return events


def raise_insolvent():
    sys.stdout.write(json.dumps({"error": 'Insolvent'}) + '\n')
    sys.exit()


if __name__ == "__main__":
    main()
