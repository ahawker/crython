__author__ = 'Andrew Hawker <andrew.r.hawker@gmail.com>'

from crython.crython import sec, min, hr, dom, mon, dow, yr
import unittest

class CronField(object):
    def test_wildcard(self):
        """
        Test field created from a wildcard (*) character.
        """
        midpt = (self.min + self.max) / 2
        field = self.field('*')
        assert midpt in field
        assert self.min in field
        assert self.max in field
        assert not (self.min - 1) in field
        assert not (self.max + 1) in field

    def test_integer(self):
        """
        Test field created from an integer object.
        """
        val = (self.max + self.min) / 2
        field = self.field(val)
        assert not (val - 1) in field
        assert not (val + 1) in field
        assert val in field

    def test_csv(self):
        """
        Test field created from a comma separated list.
        """
        min = self.min + 1
        midpt = (self.max + self.min) / 2
        max = self.max - 1
        field = self.field(','.join(map(str, (min, midpt, max))))
        assert min in field
        assert midpt in field
        assert max in field
        assert not (midpt - 1) in field
        assert not (max + 10) in field

    def test_integer_string(self):
        """
        Test field created from a string which can be converted to an integer.
        """
        val = (self.max + self.min) / 2
        field = self.field(str(val))
        assert val in field
        assert not (val - 1) in field
        assert not (val + 1) in field

    def test_range(self):
        """
        Test field created from string representation of a range.
        """
        start = self.min + 10
        stop = start + 10
        midpt = (start + stop) / 2
        field = self.field('{0}-{1}'.format(start, stop))
        assert start in field
        assert midpt in field
        assert stop in field
        assert not (start - 1) in field
        assert not (stop + 1) in field

    def test_range_with_step(self):
        """
        Test field created from string representation of a range with a step.
        """
        start = self.min + 10
        stop = start + 10
        step = 2
        field = self.field('{0}-{1}/{2}'.format(start, stop, step))
        assert start in field
        assert stop in field
        assert (start + step) in field
        assert not (stop + step) in field
        assert not (start + (step - 1)) in field
        assert not (start + (step + 1)) in field

    def test_wildcard_with_step(self):
        """
        Test field created from a wildcard with a step.
        """
        step = 2
        field = self.field('*/{0}'.format(step))
        assert self.min in field
        assert (self.min + step) in field
        assert not (self.min + 1) in field

    def test_range_obj(self):
        """
        Test field created from an iterable. Ex: range(x,y)
        """
        start = self.min
        stop = start + 20
        midpt = (start + stop) / 2
        field = self.field(range(start, stop))
        assert start in field
        assert midpt in field
        assert not stop in field
        assert not (stop + 1) in field

    def test_range_obj_with_step(self):
        """
        Test field created from an interable with step. Ex: range(x,y,z)
        """
        start = self.min
        stop = start + 20
        step = 2
        field = self.field(range(start,stop, step))
        assert start in field
        assert not stop in field
        assert (start + step) in field
        assert not (stop + step) in field
        assert not (start + (step - 1)) in field
        assert not (start + (step + 1)) in field

class TestCronSecond(unittest.TestCase, CronField):
    def setUp(self):
        self.field = sec
        self.min = 0
        self.max = 59
        self.specials = set(['*', '/', ',', '-'])

class TestCronMinute(unittest.TestCase, CronField):
    def setUp(self):
        self.field = min
        self.min = 0
        self.max = 59
        self.specials = set(['*', '/', ',', '-'])

class TestCronHour(unittest.TestCase, CronField):
    def setUp(self):
        self.field = hr
        self.min = 0
        self.max = 23
        self.specials = set(['*', '/', ',', '-'])

class TestCronDay(unittest.TestCase, CronField):
    def setUp(self):
        self.field = dom
        self.min = 1
        self.max = 31
        self.specials = set(['*', '/', ',', '-', '?', 'L', 'W'])

class TestCronMonth(unittest.TestCase, CronField):
    def setUp(self):
        self.field = mon
        self.min = 1
        self.max = 12
        self.specials = set(['*', '/', ',', '-'])

class TestCronDayOfWeek(unittest.TestCase, CronField):
    def setUp(self):
        self.field = dow
        self.min = 0
        self.max = 6
        self.specials = set(['*', '/', '-', '?', 'L', '#'])

class TestCronYear(unittest.TestCase, CronField):
    def setUp(self):
        self.field = yr
        self.min = 1970
        self.max = 2099
        self.specials = set(['*', '/', ',', '-'])

if __name__ == '__main__':
    unittest.main()