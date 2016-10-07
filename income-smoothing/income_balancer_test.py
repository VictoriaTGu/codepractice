import unittest
from datetime import datetime
from datetime import timedelta

from income_balancer import IncomeBalancer

class TestIncomeBalancer(unittest.TestCase):
    def setUp(self):
        self.start_date = datetime(2016,1,1)
        self.balancer = IncomeBalancer(self.start_date)

    def tearDown(self):
        while not self.balancer.is_empty():
            self.balancer.pop()

    def test_get_avg(self):
        self.balancer.push(self.start_date, 2, None)
        assert self.balancer.get_running_avg() == 2.0

    def test_push(self):
        self.balancer.push(self.start_date + timedelta(days=1), 5, None)
        (spendable_amount, seconds, income_obj) = self.balancer.pop()
        assert spendable_amount == -5
        assert self.balancer.is_empty()

    def test_no_realloc(self):
        self.balancer.push(self.start_date, 2, None)
        self.balancer.push(self.start_date + timedelta(days=1), 5, None)
        (spendable_amount, seconds, income_obj) = self.balancer.pop()
        assert spendable_amount == -5
        (spendable_amount, seconds, income_obj) = self.balancer.pop()
        assert spendable_amount == -2
        assert self.balancer.is_empty()

    def test_realloc_simple(self):
        self.balancer.push(self.start_date, 2, None)
        self.balancer.push(self.start_date + timedelta(days=1), 5, None)
        self.balancer.push(self.start_date + timedelta(days=2), 2, None)
        assert self.balancer.get_running_avg() == 3.0
        (spendable_amount, seconds, income_obj) = self.balancer.pop()
        assert spendable_amount == -4
        (spendable_amount, seconds, income_obj) = self.balancer.pop()
        assert spendable_amount == -3
        (spendable_amount, seconds, income_obj) = self.balancer.pop()
        assert spendable_amount == -2
        assert self.balancer.is_empty()

    def test_realloc_complex(self):
        self.balancer.push(self.start_date, 2, None)
        self.balancer.push(self.start_date + timedelta(days=1), 5, None)
        self.balancer.push(self.start_date + timedelta(days=2), 2, None)
        self.balancer.push(self.start_date + timedelta(days=3), 1, None)
        assert self.balancer.get_running_avg() == 2.5
        (spendable_amount, seconds, income_obj) = self.balancer.pop()
        assert spendable_amount == -3
        (spendable_amount, seconds, income_obj) = self.balancer.pop()
        assert spendable_amount == -2.5
        (spendable_amount, seconds, income_obj) = self.balancer.pop()
        assert spendable_amount == -2.5
        (spendable_amount, seconds, income_obj) = self.balancer.pop()
        assert spendable_amount == -2
        assert self.balancer.is_empty()

    def test_realloc_all(self):
        self.balancer.push(self.start_date, 100, None)
        self.balancer.push(self.start_date + timedelta(days=1), 100, None)
        self.balancer.push(self.start_date + timedelta(days=2), 100, None)
        self.balancer.push(self.start_date + timedelta(days=3), 100, None)
        self.balancer.push(self.start_date + timedelta(days=4), 0, None)
        assert self.balancer.get_running_avg() == 80.0
        (spendable_amount, seconds, income_obj) = self.balancer.pop()
        assert spendable_amount == -80.0
        (spendable_amount, seconds, income_obj) = self.balancer.pop()
        assert spendable_amount == -80.0
        (spendable_amount, seconds, income_obj) = self.balancer.pop()
        assert spendable_amount == -80.0
        (spendable_amount, seconds, income_obj) = self.balancer.pop()
        assert spendable_amount == -80.0
        (spendable_amount, seconds, income_obj) = self.balancer.pop()
        assert spendable_amount == -80.0
        assert self.balancer.is_empty()

    def test_to_dict(self):
        self.balancer.push(self.start_date, 2, None)
        self.balancer.push(self.start_date + timedelta(days=1), 5, None)
        tbl = self.balancer.to_dict()
        assert tbl[(self.start_date, None)] == 2
        assert tbl[(self.start_date + timedelta(days=1), None)] == 5
        assert len(tbl) == 2


if __name__ == "__main__":
    unittest.main()

