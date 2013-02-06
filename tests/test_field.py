import crython
import unittest
from crython import sec

from crython import tab

__author__ = 'Andrew Hawker <andrew.r.hawker@gmail.com>'
#
#print 'Testing single digits...'
#print 1 in sec('1')
#print 2 in sec('1') #False
#print 'Testing wildcards...'
#print 1 in sec('*')
#print 2 in sec('*')
#print '1-10' in sec('*')
#print None in sec('*')
#print 'Testing ranges...'
#print 1 in sec('1-10')
#print 5 in sec('1-10')
#print 10 in sec('1-10')
#print 11 in sec('1-10') #False
#print 'Testing ranges with steps...'
#print 1 in sec('1-10/2')
#print 2 in sec('1-10/2') #False
#print 3 in sec('1-10/2')
#print 10 in sec('1-10/2') #False
#print 11 in sec('1-10/2') #False
#print 'Testing with wildcard and steps...'
#print 1 in sec('*/2') #False
#print 2 in sec('*/2')
#print 10 in sec('*/2')
#print 0 in sec('*/2')
#print 58 in sec('*/2')
#print 59 in sec('*/2') #False
#print 60 in sec('*/2') #False
#print 'Testing comma separated values...'
#print 1 in sec('1,2,5,10')
#print 2 in sec('1,2,5,10')
#print 4 in sec('1,2,5,10') #False
#print 5 in sec('1,2,5,10')
#print 10 in sec('1,2,5,10')
#print 'Testing comma separated values with range...'
#print 1 in sec('1,2,4-10')
#print 5 in sec('1,2,4-10')
#print 6 in sec('1,2,4-10')
#print 10 in sec('1,2,4-10')
#print 12 in sec('1,2,4-10') #False
#print 'Testing comma separated values with range and step...'
#print 1 in sec('1,2,4-10/2')
#print 5 in sec('1,2,4-10/2') #False
#print 6 in sec('1,2,4-10/2')
#print 10 in sec('1,2,4-10/2')
#print 12 in sec('1,2,4-10/2') #False

class TestSecond(unittest.TestCase):
    def test_second_init(self):
        self.assertRaises(ValueError, sec, -1)
        self.assertRaises(ValueError, sec, 60)
        self.assertRaises(ValueError, sec, '?')
        self.assertRaises(ValueError, sec, 'L')
        self.assertRaises(ValueError, sec, 'W')
        self.assertRaises(ValueError, sec, '#')

    def test_second_wildcard(self):
        s = sec('*')
        assert 12 in s
        assert 0 in s
        assert 59 in s
        assert not -1 in s
        assert not 60 in s

    def test_second_integer(self):
        s = sec(20)
        assert not 19 in s
        assert not 21 in s
        assert 20 in s

    def test_second_csv(self):
        s = sec('1,5,10')
        assert 1 in s
        assert 5 in s
        assert 10 in s
        assert not 3 in s
        assert not 42 in s

    def test_second_integer_string(self):
        s = sec('42')
        assert 42 in s
        assert not 41 in s
        assert not 43 in s

    def test_second_range(self):
        s = sec('10-20')
        assert 10 in s
        assert 15 in s
        assert 20 in s
        assert not 9 in s
        assert not 21 in s

    def test_second_range_with_step(self):
        s = sec('10-20/2')
        assert 10 in s
        assert 20 in s
        assert 12 in s
        assert not 15 in s
        assert not 8 in s
        assert not 22 in s

    def test_second_wildcard_with_step(self):
        s = sec('*/2')
        assert 0 in s
        assert 2 in s
        assert 58 in s
        assert not 1 in s
        assert not 59 in s

    def test_second_obj_range(self):
        s = sec(range(0, 20))
        assert 0 in s
        assert 10 in s
        assert 20 in s  #TODO -- left failing as a reminder
        assert not 21 in s

    def test_second_obj_range_with_step(self):
        s = sec(range(0, 20, 2))
        assert 0 in s
        assert 10 in s
        assert 20 in s  #TODO -- left failing as a reminder
        assert not 11 in s
        assert not 17 in s


if __name__ == '__main__':
    unittest.main()