import crython
import unittest
from crython.crython import sec

__author__ = 'Andrew Hawker <andrew.r.hawker@gmail.com>'

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
    def test_sec_beyond_lower_bound_fail(self):
        """
        Test against less than the minimum value should raise a pre-check exception.
        """
        pass

    def test_sec_beyond_upper_bound_fail(self):
        """
        Test against less than the maximum value should raise a pre-check exception.
        """
        pass

    def test_sec_equals_lower_bound_pass(self):
        """
        Test against the minimum value supported for seconds.
        """
        pass

    def test_sec_equals_upper_bound_pass(self):
        """
        Test against the maximum value support for seconds.
        """
        pass

    def test_sec_wildcard_always_pass(self):
        """
        Test random assortment of values against the wildcard.
        """
        pass

    def test_sec_range(self):
        pass
