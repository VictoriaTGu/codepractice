## Even Financial Planner

Even plans your financial life using information about your future incomes and expenses. Specifically, it maps incomes to expenses such that all obligations are accounted for before they are due. It is also aware that we are working for _people_ and spreads excess funds over multiple pay periods to maximize the week-to-week stability of leftover income. A customer shouldn't be encouraged to spend hundreds of dollars one week when we know that the following week things will be tight.

* Our customers frequently work multiple jobs, so you'll need to support mapping funds from one or more incomes.
* Schedules vary widely: some obligations are one-time-only; some incomes are defined on an interval basis while others are defined on a monthly basis.
* Insolvency: not having enough funds to meet an obligation is possible and you must handle it by emitting an error.
* If an income and expense occur on the same day you are permitted to use the newly received funds to meet the same-day obligation.
* We've only given you a subset of our test cases. Your algorithm should work well in tight or unconventional situations. Part of the exercise is discovering where things might break and articulating cases for them.

### What are we looking for?

The goal of this exercise is twofold:

* Ascertain that you are capable of quickly solving a problem in an unfamiliar domain.
* Get a sense for what you consider to be a clean and maintainable solution.

We're hoping to see what you consider to be a "production-quality" submission. Where that isn't possible, a comment in the source code should be more than enough for us to understand what you're thinking.

### Input

Your program will accept a JSON map over STDIN that contains data about the customer. Example:

```json
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
```

* **Note**: Your submission should assume that time begins on `2016-01-01` and ends on `2016-12-30`
* We support a variety of schedules. You'll want to take a look at `complex.input.json` to get a sense for the other types we might send your way.

### Output

We expect JSON over STDOUT that describes a time series of income and expense events, with metadata for allocation mapping, instantaneous spendable funds (smoothed leftover funds, intended for discretionary spending), and savings balance (truly leftover funds).

```json
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
```

#### Insolvency

You must detect and handle this by emitting the following output:

```json
{
    "error": "Insolvent"
}
```

Easy :)

* **Bonus**: Describe how you would solve this in a real world application.

### Deliverable

You are welcome to implement your solution in the language of choice.

We expect a ZIP archive containing the following:

* `run.sh` file at the root of the archive that runs your application
* Written summary of your approach, and avenues for future development
* Additional test cases, if any
* Source code
