"""
This class encapsulates a priority queue data structure that re-balances the spendable amounts
of each of its elements every time a new income event is added so that, whenever possible,
the new income event has a spendable amount equal to or greater than the average spendable
amounts of all the elements in the queue.

It assumes that spendable amounts are pushed into the queue sequentially in time and that
spendable income can only be distributed forward in time.

The balancer also will NOT take so much money from a prior income source that the prior income
source now has a spendable amount less than the average spendable amount.

E.G. (This example also appears in income_balancer_test.py)
Push(Income(200))
Push(Income(500)) # this is greater than avg 350 so nothing is done
Push(Income(200)) # this is less than avg 300 so push 100 from 500 to 200

The elements are now:
    Income(200)
    Income(400)
    Income(300) # which is now >= avg 300

Now we push a fourth element:
Push(Income(100)) # this is less than avg 250 so push 150 from 400 to 100

The elements are now:
    Income(200)
    Income(250)
    Income(300)
    Income(250) # which is now >= avg 250
"""

from datetime import datetime
from datetime import timedelta
from heapq import heappush
from heapq import heappop


class IncomeBalancer(object):
    priorityq = []
    running_sum = 0.0
    num_elements = 0

    def is_empty(self):
        return len(self.priorityq) == 0

    def push(self, new_spendable_amount, secondary_index):
        amount_distributed_from_other_sources = self.reallocate_spendable_amounts(new_spendable_amount)
        self.running_sum += new_spendable_amount
        self.num_elements += 1
        spendable_amount = new_spendable_amount + amount_distributed_from_other_sources
        # have to negate the priority keys because heapq only implements min-heap
        heappush(self.priorityq, (-spendable_amount, -secondary_index))

    def get_running_avg(self):
        return self.running_sum / self.num_elements if self.num_elements else None

    def reallocate_spendable_amounts(self, new_spendable_amount):
        new_running_avg = (self.running_sum + new_spendable_amount) / (self.num_elements+1)
        amount_distributed_from_other_sources = 0.0
        # if less than new avg, then redistribute from the income sources already in the queue
        if new_spendable_amount < new_running_avg:
            amount_to_redistribute = new_running_avg - new_spendable_amount
            temporary_queue = []
            while amount_to_redistribute > 0.0 and len(self.priorityq) > 0:
                (spendable_amount, secondary_index) = heappop(self.priorityq)
                spendable_amount = abs(spendable_amount)
                amount_in_excess_of_avg = max([spendable_amount - new_running_avg, 0.0])
                reallocation_amount = min([amount_in_excess_of_avg, amount_to_redistribute])
                heappush(temporary_queue, (-(spendable_amount - reallocation_amount), secondary_index))
                amount_to_redistribute -= reallocation_amount
                amount_distributed_from_other_sources += reallocation_amount
            # push back into main queue
            while len(temporary_queue) > 0:
                queue_obj = heappop(temporary_queue)
                heappush(self.priorityq, queue_obj)
        return amount_distributed_from_other_sources

    def pop(self):
        (spendable_amount, secondary_index) = heappop(self.priorityq)
        self.running_sum -= spendable_amount
        self.num_elements -= 1
        return (abs(spendable_amount), abs(secondary_index))

    def to_dict(self):
        event_to_spendable_amount = {}
        while len(self.priorityq) > 0:
            (spendable_amount, secondary_index) = heappop(self.priorityq)
            event_to_spendable_amount[abs(secondary_index)] = abs(spendable_amount)
        return event_to_spendable_amount
