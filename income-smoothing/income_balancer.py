from datetime import datetime
from datetime import timedelta
from heapq import heappush
from heapq import heappop


class IncomeBalancer(object):
    priorityq = []
    running_sum = 0.0
    num_elements = 0

    def __init__(self, start_date):
        self.start_date = start_date

    def is_empty(self):
        return len(self.priorityq) == 0

    def push(self, date, spendable_amount, income_obj):
        amount_distributed_from_other_sources = self.reallocate_spendable_amounts(spendable_amount)
        self.running_sum += spendable_amount
        self.num_elements += 1
        spendable_amount += amount_distributed_from_other_sources
        seconds_since_start_date = (date - self.start_date).total_seconds()
        heappush(self.priorityq, (-spendable_amount, -seconds_since_start_date, income_obj))

    def get_running_avg(self):
        return self.running_sum / self.num_elements if self.num_elements else None

    def reallocate_spendable_amounts(self, new_spendable_amount):
        new_running_avg = (self.running_sum + new_spendable_amount) / (self.num_elements+1)
        # if less than avg, then redistribute from the income sources already in the queue
        amount_distributed_from_other_sources = 0.0
        if new_spendable_amount < new_running_avg:
            amount_to_redistribute = new_running_avg - new_spendable_amount
            temporary_queue = []
            while amount_to_redistribute > 0.0 and len(self.priorityq) > 0:
                (spendable_amount, seconds, income_obj) = heappop(self.priorityq)
                spendable_amount = abs(spendable_amount)
                amount_in_excess_of_avg = max([spendable_amount - new_running_avg, 0.0])
                reallocation_amount = min([amount_in_excess_of_avg, amount_to_redistribute])
                heappush(temporary_queue, (-(spendable_amount - reallocation_amount), seconds, income_obj))
                amount_to_redistribute -= reallocation_amount
                amount_distributed_from_other_sources += reallocation_amount
            # push back into main queue
            while len(temporary_queue) > 0:
                queue_obj = heappop(temporary_queue)
                heappush(self.priorityq, queue_obj)
        return amount_distributed_from_other_sources

    def pop(self):
        (spendable_amount, seconds, income_obj) = heappop(self.priorityq)
        self.running_sum -= spendable_amount
        self.num_elements -= 1
        return (spendable_amount, seconds, income_obj)

    def to_dict(self):
        event_to_spendable_amount = {}
        while len(self.priorityq) > 0:
            (spendable_amount, seconds, income_obj) = heappop(self.priorityq)
            date = self.start_date + timedelta(seconds=abs(seconds))
            event_to_spendable_amount[(date, income_obj)] = abs(spendable_amount)
        return event_to_spendable_amount





