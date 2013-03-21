__author__ = 'Andrew Hawker <andrew.r.hawker@gmail.com>'

from crython.crython import CronExpression
import unittest

class TestCronExpression(unittest.TestCase):
    ATTRIBUTES = 'second minute hour day month weekday year'.split()

    @classmethod
    def has_all_attributes(cls, expr):
        return all(k in expr.__dict__ for k in cls.ATTRIBUTES)

    @classmethod
    def setUpClass(cls):
        cls.default = CronExpression()
        cls.wildcard = CronExpression(expr='* * * * * * *')

        def keywords():
            for k,v in CronExpression.KEYWORDS.items():
                yield k.strip('@'), CronExpression(expr=v)
        cls.keywords = dict(keywords())

    def test_keywords(self):
        for k,v in self.keywords.items():
            assert CronExpression(expr='@{0}'.format(k)) == v

    def test_attributes(self):
        assert self.has_all_attributes(self.default)
        assert self.has_all_attributes(self.wildcard)
        assert all(map(self.has_all_attributes, self.keywords.values()))

    def test_init_empty(self):
        assert self.default == self.wildcard

    def test_init_expr(self):
        pass

    def test_wildcard_defaults(self):
        pass


if __name__ == '__main__':
    unittest.main()