## Summary of Approach 

### Handling different types of scheduled income and expenses
I first started out with a base class called ScheduledEvent which would serve
as the base class which would inherit common attributes (like name, amount, etc.) and
expose a factory method that would generate instances of sub-classes of ScheduledEvent
(like MonthlyEvent) based on event frequency. Each sub-class of ScheduledEvent would
implement the method `get_amount_on_date(date)`, which would allow me to generate
a timeseries of incomes and expenses over any date range.

I chose this design because it's easily extendable to new types of income and
expense schedules (just create another sub-class that extends ScheduledEvent), and
it minimizes redundant code (ScheduledEvent contains common code and attributes).

### Allocations and Sources
This is mostly a repeat of the comments above the function `get_allocations_and_sources`

First, the algorithm would keep track of how much non-allocated income is available per
week. Non-allocated means the amount that is not already assigned to meet a specific
expense. This was simply stored in an array that is updated as the income sources
come in chronological order.

On each day, iterate over the income sources that arrive that day, update the
non-allocated amount per week, and then decide which week to pull non-allocated income
from in order to meet the expenses for that day. For example, if the weekly income
array so far is [450, 960, 0, 0], then the algorithm would choose week index 1.
The algorithm keeps a hashtable mapping week indices to priority queues (each week
has one, and it stores income sources for that week). Each income source would be
prioritized based on how much non-allocated income is left over. If the expense is
600 dollars, then it would pull income sources from the priority queue for week 1
until either it has pulled 600 dollars or it has exhausted the sources from week 1
and must turn to sources from another week.

The reason for choosing these priority keys is to enable a greedy algorithm to
roughly even out non-allocated amounts left over during the allocation.

Allocations are stored using a hash table mapping (date, income) to expense, with
metadata on how much is allocated from that income source to that particular expense
and the date of the expense. Similarly, sources are stored using a hash table mapping
(date, expense) to income source, with metadata on how much was allocated and the date
of the income source.

### Insolvency
Each time the algorithm is trying to assign an expense to an income source, if the
sum of the array tracking weekly non-allocated income is zero, then that means
the expense cannot be satisfied using any income sources that arrived on that day
or prior to that day while also satisfying any previous expenses.

### Income Smoothing
This is a repeat of the comments above the `IncomeSmoother` class.

This class encapsulates a priority queue data structure that re-balances the amounts
of each of its elements every time a new amount is added so that, whenever possible,
the new income event has a amount equal to or greater than the average amounts
of all the elements in the queue.

It assumes that amounts are pushed into the queue sequentially in time and that
income can only be distributed forward in time (you can save income and use it in the future,
but you can't take income from the future and use it in the present).

The smoother also will NOT take so much money from a prior income source that the prior income
source now has a amount less than the average amount.

e.g. (This example also appears in income_smoother_test.py)

Push(200)

Push(500) # this is greater than avg 350 so nothing is done

Push(200) # this is less than avg 300 so push 100 from 500 to 200

The elements are now:

    (200)

    (400)
    
    (300) # which is now >= avg 300

Now we push a fourth element:

Push(100) # this is less than avg 250 so push 150 from 400 to 100

The elements are now:

    (200)
    
    (250)

    (300)

    (250) # which is now >= avg 250

#### How It Is Used 
The IncomeSmoother interface is generic enough that you could push income events as they
arrive in chronological order, but considering that multiple income sources are possible
it made more sense to push weekly nonallocated income amounts so that it would smooth
the weekly nonallocated income rather than just smoothing individual income events.

The `smoother.to_dict()` then returns a mapping of week indices to spendable income,
which is income minus allocations for expenses and the amount saved for future weeks.
The `generate_timeseries` function then uses this to determine, as it iterates through
income sources, how much to assign to spendable based on what week it occurs.

## In a Production Environment

### Handling Streaming Events
A production environment would probably need to take in a stream of events coming in (income
sources and expenses with expected schedules) for many people, use the factory function to
translate them into sub-classes of ScheduledEvent, and then store them into database
tables with user id as a foreign key. Kafka would be one such tool for taking in streaming
events and moving them through this pipeline.

### Assigning Allocations and Sources
The current implementation requires heap space for tracking weekly nonallocated income and
a min-heap or max-heap for storing income sources. The production implementation depends
on whether you're running this simulation just once per year for each person or whether
it has to be run again every time an unexpected income or expense comes in. It also
depends on whether it's user-facing (needs to display results to the user quickly) or
can be run offline. 

It's possible to run this simulator on many thousands of threads (one for each person) and
store the allocations, sources, spendable and saved amounts in separate database tables for easy
lookup. Then, whenever an expected income source or expense shows up, you can then look up which
expenses to allocate it to, how much of it to save, etc.

If the simulator is often re-run, though, you would want to avoid running the simulator over
and over again each time an unexpected income source or expense shows up. I'm assuming that a real
life use case would look like this: You have a set of expected incomes and expenses and have already
run the simulator for the year of 2016 to allocate future incomes and expenses and saved amounts.
However, one day a few months into 2016, an unexpected expense appears and it's scheduled to be
a new monthly expense. You can avoid a lot of unnecessary computations by starting the simulator
on the day it left off and with memory of the nonallocated amounts per week and income sources
that have not yet been exhausted. This could be done using a cached database lookup using memcached
(might work well if you have a high rate of cache hits).

### Smoothing Income
If you had to re-run the simulator when unexpected events occur, the IncomeSmoother class would
have to be modified so that previous weeks' spending cannot be modified and only the current and
future weeks' spending can be modified to smooth over future predicted income.

Similar to the assignment of allocations and sources, it would be faster to retrieve the smoother
at the current day (instead of replaying every day in 2016) or the last day before that it left off
and this could be done using a cached database lookup.

## Future Improvements
If I had more time I would work more on the income smoothing. One issue that comes up in the current
algorithm is the outlier and cold start problem, which is that it doesn't do a great job of smoothing
income in the first few weeks if the first few weeks have significantly less nonallocated income than
future weeks. Overall, any weeks that are significantly different than the overall average will
make it difficult for the income smoother to get a good read on what the average weekly spending
should look like because it significantly changes the average.

In the complex.input.json output, the weekly nonallocated income looks like this: 

[20.0, 0.0, 360.0, 0.0, 360.0, 0.0, 340.0, 0.0, 380.0, 0.0, 340.0, 0.0, 300.0, 320.0, 320.0, 340.0,
300.0, 360.0, 200.0, 340.0, 300.0, 360.0, 400.0, 320.0, 400.0, 0.0, 420.0, 0.0, 400.0, 0.0, 480.0,
0.0, 440.0, 0.0, 420.0, 0.0, 440.0, 0.0, 400.0, 420.0, 400.0, 440.0, 400.0, 360.0, 400.0, 440.0,
400.0, 360.0, 400.0, 640.0, 400.0, 0.0, 0.0]

The spendable income (minus savings) with smoothing by week looks like this (the key is the week index):

{0: 10.0, 1: 10.0, 2: 265.0, 3: 95.0, 4: 236.66666666666669, 5: 123.33333333333333, 6: 205.0,
7: 135.0, 8: 234.0, 9: 146.0, 10: 190.0, 11: 150.0, 12: 300.0, 13: 320.0, 14: 320.0, 15: 303.3333333333333,
16: 300.0, 17: 293.96491228070175, 18: 207.3684210526316, 19: 321.1764705882353, 20: 300.0,
21: 317.14285714285717, 22: 318.05668016194335, 23: 320.0, 24: 233.07692307692307, 25: 233.07692307692307,
26: 231.42857142857142, 27: 231.42857142857142, 28: 229.33333333333334, 29: 229.33333333333334, 30: 250.0,
31: 230.0, 32: 229.41176470588235, 33: 229.41176470588235, 34: 228.33333333333334, 35: 228.33333333333334,
36: 227.89473684210526, 37: 227.89473684210526, 38: 400.0, 39: 420.0, 40: 400.0, 41: 347.16981132075466,
42: 400.0, 43: 360.0, 44: 400.0, 45: 266.41509433962267, 46: 400.0, 47: 360.0, 48: 400.0,
49: 368.46153846153845, 50: 400.0, 51: 271.53846153846155, 52: 266.41509433962267}

As you can see, the nonallocated income in the first two weeks is low, so the algorithm thinks
the average nonallocated income is low for the next 4-6 weeks until it gets enough data points
to get a better estimate of the normal week by week average. Even so, the algorithm keeps all
the data points in memory when in fact it might be better for the algorithm to keep only what
it considers to be 'normal' or within some number of standard deviations of what is expected.
It could also only keep track of the running average of the last N data points, so the effect
of outlier data points is limited. Finally, the algorithm could try to use the median as its
estimate so that it's even more robust against outlier data points.
