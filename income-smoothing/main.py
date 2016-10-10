"""Usage: cat simple.input.json | python main.py
This file takes in information describing scheduled incomes and expenses in
json format (example below) and writes a timeseries of incomes and expenses
(with metadata on how income events are allocated to expenses and appropriate
spendable amounts of each income source) to stdout in json format.

Input example:
{
    "incomes": [
        {
            "name": "Starbucks",
            "amount": 200.00,
            "schedule": {
                "type": "interval",
                "period": 14,
                "start": "2016-01-01"
            }
        }
    ],
    "expenses": [
        {
            "name": "Rent",
            "amount": 100.00,
            "schedule": {
                "type": "interval",
                "period": 14,
                "start": "2016-01-01"
            }
        }
    ]
}

Output example:
{
    "events": [
        {
            "type": "income",
            "name": "Starbucks",
            "date": "2016-01-15",
            "allocations": [
                {
                    "name": "Rent",
                    "date": "2016-01-15",
                    "amount": 100.00
                }
            ],
            "spendable": 100.00,
            "saved": 0.00
        },
        {
            "type": "expense",
            "name": "Rent",
            "date": "2016-01-15",
            "sources": [
                {
                    "name": "Starbucks",
                    "date": "2016-01-15",
                    "amount": 100.00
                }
            ]
        }
        // ... etc ...
    ]
}

"""
from collections import defaultdict
from copy import deepcopy
from datetime import datetime
from datetime import timedelta
from heapq import heappush
from heapq import heappop
import json
import sys

from classes import DATE_FORMAT
from classes import ScheduledEvent
from income_balancer import IncomeBalancer

START_DATE = '2016-01-01'
AMOUNT_FORMAT = '{0:.2f}'
NUM_DAYS_IN_TIMESERIES = 365


def main():
    json_dict = json.load(sys.stdin)
    scheduled_income = parse_events(json_dict['incomes'], 'income')
    scheduled_expenses = parse_events(json_dict['expenses'], 'expense')
    start_date = datetime.strptime(START_DATE, DATE_FORMAT)
    dates_in_year = [
        start_date + timedelta(days=i) for i in xrange(NUM_DAYS_IN_TIMESERIES)
    ]
    allocations, sources = get_allocations_and_sources(
        dates_in_year, scheduled_income, scheduled_expenses
    )
    week_index_to_spendable_amount = get_smoothed_spendable_income(
        dates_in_year, scheduled_income, allocations
    )
    events = generate_timeseries(
        start_date, dates_in_year, allocations, sources, scheduled_income,
        scheduled_expenses, week_index_to_spendable_amount
    )
    sys.stdout.write(
        json.dumps({"events": events}, indent=4, separators=(',', ': '))
        + '\n'
    )


def parse_events(events, event_type):
    """Map a list of dictionaries to a list of instances of sub-classes
    of ScheduledEvent (ie MonthlyEvent, IntervalEvent)

    :param events: list of dictionaries describing incomes and expenses
    :type events: list of dictionaries
    :param event_type: income or expense
    :type event_type: string

    :returns: list of scheduled income sources or expenses
    :rtype: list of sub-classes of ScheduledEvent
    """
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


def get_allocations_and_sources(dates, scheduled_income, scheduled_expenses):
    """First, keep track of how much non-allocated income is available per week.
    Non-allocated means the amount that is not already assigned to meet a specific
    expense. This was simply stored in an array that is updated as the income sources
    come in chronological order.

    On each day, iterate over the income sources that arrive that day and update the
    non-allocated amount per week. Then, for each expense that day, decide which week
    to pull non-allocated income from in order to meet that expense.
    For example, if the weekly income array so far is [450, 960, 0, 0], then the
    algorithm would choose week index 0.

    The algorithm keeps a hashtable mapping week indices to priority queues (each week
    has one, and it stores income sources for that week). Each income source would be
    prioritized based on how much non-allocated income is left over. If the expense is
    600 dollars, then it would pull income sources from the priority queue for week 1
    until either it has pulled 600 dollars or it has exhausted the sources from week 1
    and must turn to sources from another week.

    :param dates: list of datetime.datetimes in chronological order
    :type dates: list of datetime.datetimes
    :param scheduled_income: list of scheduled incomes
    :type scheduled_income: list of sub-classes of ScheduledEvent (e.g. MonthlyEvent)
    :param scheduled_expenses: list of scheduled expenses
    :type scheduled_expenses: list of sub-classes of ScheduledEvent (e.g. MonthlyEvent)

    :returns:
        allocations:
            a dictionary mapping (date, scheduled income) to a list of expenses
            with metadata on the amount allocated to that specific expense and the date of
            the expenses
        sources:
            a dictionary mapping (date, scheduled expense) to a list of income sources with
            metadata on the amount allocated from that income source to the expense and
            the date of the income event
    :rtype:
        allocations:
            dict((datetime.datetime, sub-class of ScheduledEvent), [dicts with metadata])
        sources:
            dict((datetime.datetime, sub-class of ScheduledEvent), [dicts with metadata])
    """
    allocations, sources = defaultdict(list), defaultdict(list)
    start_date = dates[0] if dates else None
    end_date = dates[-1] if dates else None
    num_weeks = (end_date - start_date).days // 7 if dates else -1
    week_index_to_sources_queue = defaultdict(list)
    weekly_nonallocated_amounts = [0.0] * (num_weeks+1)

    for date in dates:
        for income in scheduled_income:
            amount = income.get_amount_on_date(date)
            if amount is not None:
                week_index = (date - start_date).days // 7
                # have to negate the priority keys because heapq only implements min-heap
                heappush(week_index_to_sources_queue[week_index], (-amount, date, income))
                weekly_nonallocated_amounts[week_index] += amount

        for expense in scheduled_expenses:
            amount_owed = expense.get_amount_on_date(date)
            while amount_owed is not None and amount_owed > 0:
                if sum(weekly_nonallocated_amounts) <= 0.0:
                    raise_insolvent()
                amount_extracted, income_with_metadata = match_income_source(
                    weekly_nonallocated_amounts,
                    week_index_to_sources_queue,
                    amount_owed
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


def match_income_source(
    weekly_nonallocated_amounts, week_index_to_sources_queue, amount_owed
):
    """Pick the week with the largest un-allocated balance, pick an income source from
    that week, and allocate as much as possible to satisfy the amount owed on the expense.
    Finally, return the amount allocated as well as the metadata on the income source

    :param weekly_nonallocated_amounts: array tracking non-allocated amounts per week
    :type weekly_nonallocated_amounts: list of floats
    :param week_index_to_sources_queue: dict mapping week index to priority queue
    with available sources of income
    :type week_index_to_sources_queue: dict(index, priority queue)
    :param amount_owed: amount owed on the expense
    :type amount_owed: float

    :returns: amount extracted from a single income source, metadata on the income source
    :rtype: float, dict
    """
    max_nonallocated_amount = max(weekly_nonallocated_amounts)
    week_index_of_max_amount = weekly_nonallocated_amounts.index(max_nonallocated_amount)
    sources_queue = week_index_to_sources_queue[week_index_of_max_amount]
    (amount_leftover, date, income) = heappop(sources_queue)
    amount_leftover = abs(amount_leftover)
    amount_extracted = min([amount_leftover, amount_owed])
    amount_leftover -= amount_extracted
    weekly_nonallocated_amounts[week_index_of_max_amount] -= amount_extracted
    if amount_leftover > 0.0:
        heappush(sources_queue, (-amount_leftover, date, income))
    income_with_metadata = {
        'date': date, 'event': income, 'amount_allocated': amount_extracted
    }
    return amount_extracted, income_with_metadata


def get_smoothed_spendable_income(dates, scheduled_income, allocations):
    """Push each scheduled income event as it occurs to an income balancer
    that smooths the spendable income (after allocations) from earlier
    income events to later income events.

    :param dates: list of datetime.datetimes, sequential in time
    :type dates: list of datetime.datetimes
    :param scheduled_income: list of scheduled income events
    :type scheduled_income: list of sub-classes of ScheduledEvent
    :param allocations: dict mapping (date, income) to list of expenses with metadata
    :type allocations:
            dict((datetime.datetime, sub-class of ScheduledEvent), [dicts with metadata])

    :returns: dict mapping (date, income) to appropriate spendable amount
        (after allocations and savings for smoothing future income)
    :rtype: dict((datetime.datetime, sub-class of ScheduledEvent), float)
    """
    start_date = dates[0] if dates else None
    last_date = dates[-1] if dates else None
    num_weeks = (last_date - start_date).days // 7 if dates else -1
    weekly_nonallocated_income = [0.0] * (num_weeks + 1)
    for date in dates:
        for income in scheduled_income:
            if income.get_amount_on_date(date):
                week_index = (date - start_date).days // 7
                weekly_nonallocated_income[week_index] += get_nonallocated_income(
                    date, income, allocations
                )
    balancer = IncomeBalancer()
    for week_index, nonallocated_income in enumerate(weekly_nonallocated_income):
        balancer.push(nonallocated_income, week_index)
    return balancer.to_dict()


def get_nonallocated_income(date, income, allocations):
    """Get the income amount from a specific source on a specific date, minus any
    allocations to expenses

    :param date: date of income
    :type date: datetime.datetime
    :param income: scheduled income object
    :type income: sub-class of ScheduledEvent
    :param allocations: dict mapping (date, income) to list of expenses
    :type allocations:
        dict((datetime.datetime, sub-class of ScheduledEvent), [dicts with metadata])

    :returns: income amount minus any allocations to expenses
    :rtype: float
    """
    nonallocated_income = 0.0
    amount = income.get_amount_on_date(date)
    if amount is not None:
        nonallocated_income = float(amount) - sum([
            allocation['amount_allocated'] for allocation in allocations[(date, income)]
        ])
    return nonallocated_income


def generate_timeseries(
    start_date,
    dates,
    allocations,
    sources,
    scheduled_income,
    scheduled_expenses,
    week_index_to_spendable_amount
):
    """Generate formatted dictionaries describing a timeseries of income and
    expense events, with metadata using previously assigned allocations and
    smoothed spendable amounts

    :param start_date: first date in time series
    :type start_date: datetime.datetime
    :param dates: list of dates in sequential time order
    :type dates: list of datetime.datetimes
    :param allocations: dict mapping (date, income) to list of expenses
    :type allocations:
        dict((datetime.datetime, sub-class of ScheduledEvent), [dicts with metadata])
    :param sources: dict mapping (date, expense) to list of sources
    :type sources:
        dict((datetime.datetime, sub-class of ScheduledEvent), [dicts with metadata])
    :param scheduled_income: list of scheduled income event objects
    :type scheduled_income: list of sub-classes of ScheduledEvent
    :param scheduled_expense: list of scheduled expense event objects
    :type scheduled_expense: list of sub-classes of ScheduledEvent
    :param week_index_to_spendable_amount: dict mapping week index to
        smoothed spendable amount
    :type week_index_to_spendable_amount:
        dict(int, float)

    :returns: list of dictionaries, each describing an income or expense event
    :rtype: list of dict
    """
    events = []
    for date in dates:
        for income in scheduled_income:
            if income.get_amount_on_date(date):
                spendable, amount_to_save = calculate_spendable_and_saved(
                    date, income, start_date, allocations, week_index_to_spendable_amount
                )
                events.append(generate_formatted_income_dict(
                    income, date, amount_to_save, spendable, allocations
                ))
        for expense in scheduled_expenses:
            if expense.get_amount_on_date(date):
                events.append(generate_formatted_expense_dict(
                    expense, date, sources
                ))
    return events


def calculate_spendable_and_saved(date, income, start_date, allocations, week_index_to_spendable_amount):
    """Calculate the spendable amount for a specific scheduled income and date where
    spendable = (amount - amount allocated to expenses - amount saved) and saved amount
    """
    spendable = get_nonallocated_income(date, income, allocations)
    week_index = (date - start_date).days // 7
    spendable_after_smoothing = week_index_to_spendable_amount[week_index]
    amount_to_save = max([0.0, spendable - spendable_after_smoothing])
    spendable -= amount_to_save
    week_index_to_spendable_amount[week_index] -= spendable
    return spendable, amount_to_save


def generate_formatted_income_dict(income, date, amount_to_save, spendable, allocations):
    """Insert metadata about the date of income received, amount saved, spent, and allocations"""
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
    """Insert metadata about the date of expense, date, and sources"""
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
    """Raise when an expense appears for which it's impossible to allocate enough income
    from prior income received (minus prior paid expenses)
    """
    sys.stdout.write(json.dumps({"error": 'Insolvent'}) + '\n')
    sys.exit()


if __name__ == "__main__":
    main()
