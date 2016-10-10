import unittest
from datetime import datetime
from datetime import timedelta

from income_smoother import IncomeSmoother

SECONDARY_INDEX = 0

class TestIncomeSmoother(unittest.TestCase):
    def setUp(self):
        self.balancer = IncomeSmoother()

    def tearDown(self):
        while not self.balancer.is_empty():
            self.balancer.pop()

    def test_get_avg(self):
        self.balancer.push(2, SECONDARY_INDEX)
        assert self.balancer.get_running_avg() == 2.0

    def test_push(self):
        self.balancer.push(5, SECONDARY_INDEX)
        (spendable_amount, secondary_index) = self.balancer.pop()
        assert spendable_amount == 5
        assert self.balancer.is_empty()

    def test_no_realloc(self):
        self.balancer.push(2, SECONDARY_INDEX)
        self.balancer.push(5, SECONDARY_INDEX)
        (spendable_amount, secondary_index) = self.balancer.pop()
        assert spendable_amount == 5
        (spendable_amount, secondary_index) = self.balancer.pop()
        assert spendable_amount == 2
        assert self.balancer.is_empty()

    def test_realloc_simple(self):
        self.balancer.push(2, SECONDARY_INDEX)
        self.balancer.push(5, SECONDARY_INDEX)
        self.balancer.push(2, SECONDARY_INDEX)
        assert self.balancer.get_running_avg() == 3.0
        (spendable_amount, secondary_index) = self.balancer.pop()
        assert spendable_amount == 4
        (spendable_amount, secondary_index) = self.balancer.pop()
        assert spendable_amount == 3
        (spendable_amount, secondary_index) = self.balancer.pop()
        assert spendable_amount == 2
        assert self.balancer.is_empty()

    def test_realloc_complex(self):
        self.balancer.push(2, SECONDARY_INDEX)
        self.balancer.push(5, SECONDARY_INDEX)
        self.balancer.push(2, SECONDARY_INDEX)
        self.balancer.push(1, SECONDARY_INDEX)
        assert self.balancer.get_running_avg() == 2.5
        (spendable_amount, secondary_index) = self.balancer.pop()
        assert spendable_amount == 3
        (spendable_amount, secondary_index) = self.balancer.pop()
        assert spendable_amount == 2.5
        (spendable_amount, secondary_index) = self.balancer.pop()
        assert spendable_amount == 2.5
        (spendable_amount, secondary_index) = self.balancer.pop()
        assert spendable_amount == 2
        assert self.balancer.is_empty()

    def test_realloc_all(self):
        self.balancer.push(100, SECONDARY_INDEX)
        self.balancer.push(100, SECONDARY_INDEX)
        self.balancer.push(100, SECONDARY_INDEX)
        self.balancer.push(100, SECONDARY_INDEX)
        self.balancer.push(0, SECONDARY_INDEX)
        assert self.balancer.get_running_avg() == 80.0
        (spendable_amount, secondary_index) = self.balancer.pop()
        assert spendable_amount == 80.0
        (spendable_amount, secondary_index) = self.balancer.pop()
        assert spendable_amount == 80.0
        (spendable_amount, secondary_index) = self.balancer.pop()
        assert spendable_amount == 80.0
        (spendable_amount, secondary_index) = self.balancer.pop()
        assert spendable_amount == 80.0
        (spendable_amount, secondary_index) = self.balancer.pop()
        assert spendable_amount == 80.0
        assert self.balancer.is_empty()

    def test_to_dict(self):
        self.balancer.push(2, SECONDARY_INDEX)
        self.balancer.push(5, SECONDARY_INDEX+1)
        tbl = self.balancer.to_dict()
        assert tbl[SECONDARY_INDEX] == 2
        assert tbl[SECONDARY_INDEX+1] == 5
        assert len(tbl) == 2


if __name__ == "__main__":
    unittest.main()

