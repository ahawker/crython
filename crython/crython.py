__author__ = 'Andrew Hawker <andrew.r.hawker@gmail.com>'

import calendar
import functools
import logging
import re
import datetime
import threading
import collections
import time

LOG = logging.getLogger(__name__)

DAY_NAME = dict((v.lower(),k) for k,v in enumerate(calendar.day_name))      #(ex: Monday, Tuesday, etc)
DAY_ABBR = dict((v.lower(),k) for k,v in enumerate(calendar.day_abbr))      #(ex: Mon, Tue, etc)
MON_NAME = dict((v.lower(),k) for k,v in enumerate(calendar.month_name))    #(ex: January, February, etc)
MON_ABBR = dict((v.lower(),k) for k,v in enumerate(calendar.month_abbr))    #(ex: Jan, Feb, etc)
PHRASES  = dict(DAY_NAME.items() + DAY_ABBR.items() + MON_NAME.items() + MON_ABBR.items())
PHRASES_REGEX = re.compile('|'.join(PHRASES.keys()).lstrip('|'), flags=re.IGNORECASE)

class CronField(object):
    SPECIALS   = set(['*', '/', '%', ',', '-', 'L', 'W', '#', '?'])

    def __init__(self, *args):
        self.value, self.min, self.max, self.specials = args
        if isinstance(self.value, (int, long)):                     #numbers must be within bounds
            if not self.min <= self.value <= self.max:
                raise ValueError('Value must be between {0} and {1}'.format(self.min, self.max))
        if isinstance(self.value, basestring):                      #sub name/abbr for month/dayofweek
            self.value = CronField.sub_english_phrases(self.value)
            invalid_chars = self.SPECIALS.difference(self.specials).intersection(set(self.value))
            if invalid_chars:
                raise ValueError('Field contains invalid special characters: {0}'.format(','.join(invalid_chars)))
        elif isinstance(self.value, collections.Iterable):          #sort iterables
            self.value = sorted(self.value)

    def __repr__(self):
        return '<CronField: {0}>'.format(self)
    def __str__(self):
        if isinstance(self.value, collections.Iterable) and len(self.value) >= 5:
            return '[{0}...{1}]'.format(self.value[0], self.value[-1])
        return str(self.value)

    def __contains__(self, item):
        """
        Determines if the given time is 'within' the time denoted by this individual field.
        """
        value = self.value
        if isinstance(value, (int, long)):                          #standard numeric (python obj)
            return value == item
        if isinstance(value, basestring):
            result = False
            for value in value.split(','):                          #comma separated values (ex: 1,4,10)
                value = re.split(r'[-/]', value)                    #separate range and step characters
                if len(value) == 1:
                    if value[0] == '*':                             #single wildcard (ex: *)
                        return self.min <= item <= self.max
                    result |=  int(value[0]) == item                #single digit (ex: 10)
                    continue
                if value[0] == '*':                                 #wildcard w/ step (ex: */2 ==> 0-59/2)
                    value = [self.min, self.max, value[1]]
                start, stop = sorted(map(int, value[:2]))           #range (ex: 0-10)
                step = int(value[2]) if len(value) > 2 else None    #range w/ step (ex: 0-10/2)
                result |= start <= item <= stop and (not step or (item + start) % step == 0)
            return result
        if isinstance(value, collections.Iterable):                 #iterable (assumed range() python obj)
            return item in value

    @staticmethod
    def sub_english_phrases(value):
        """
        Replace any full or abbreviated english dow/mon phrases (Jan, Monday, etc) from the field value
        with its respective integer representation.
        """
        def _repl(match):
            return str(PHRASES[match.group(0).lower()])
        return PHRASES_REGEX.sub(_repl, str(value))

#funcs for field creation so we don't need to subclass CronField with min/max/specials
sec = lambda v: CronField(v, 0,    59,   set(['*', '/', ',', '-']))
min = lambda v: CronField(v, 0,    59,   set(['*', '/', ',', '-']))
hr  = lambda v: CronField(v, 0,    23,   set(['*', '/', ',', '-']))
dom = lambda v: CronField(v, 1,    31,   set(['*', '/', ',', '-', '?', 'L', 'W']))
mon = lambda v: CronField(v, 1,    12,   set(['*', '/', ',', '-']))
dow = lambda v: CronField(v, 0,    6,    set(['*', '/', ',', '-', '?', 'L', '#']))
yr  = lambda v: CronField(v, 1970, 2099, set(['*', '/', ',', '-']))

class CronExpression(object):
    STRUCT_TIME = ('year', 'month', 'day', 'hour', 'minute', 'second', 'weekday')           #time.struct_time fields
    FIELD_NAMES = ('second', 'minute', 'hour', 'day', 'month', 'weekday', 'year', 'expr')   #supported kwargs
    FIELDS = dict(zip(FIELD_NAMES, (sec, min, hr, dom, mon, dow, yr)))                      #field name->init func
    KEYWORDS = {'@yearly':   '0 0 0 1 1 *',
                '@annually': '0 0 0 1 1 *',
                '@monthly':  '0 0 0 1 * *',
                '@weekly':   '0 0 0 * * 0',
                '@daily':    '0 0 0 * * *',
                '@hourly':   '0 0 * * * *',
                '@minutely': '0 * * * * *',
                '@reboot':   None} #TODO

    def __init__(self, **kwargs):
        expression = kwargs.get('expr')
        if expression.startswith('@'):
            expression = self.KEYWORDS.get(expression, '* * * * * * *')
        
        expression = dict(zip(self.FIELD_NAMES, expression.split()))
        for field, ctor in self.FIELDS.items():
            setattr(self, field, ctor(kwargs.get(field, expression.get(field, '*'))))

    def __repr__(self):
        return '<CronExpression: {0}>'.format(self)
    def __str__(self):
        return '{second} {minute} {hour} {day} {month} {weekday} {year}'.format(**self.__dict__)

    def __contains__(self, item): #item should always be a datetime #XXX confirm and revise
        if not isinstance(item, datetime.datetime): #hrm
            return False
        item = dict(zip(self.STRUCT_TIME, item.timetuple()[:7]))
        return all(item[k] in v for k,v in self.__dict__.items())

class CronTab(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(CronTab, self).__init__(*args, **kwargs)
        self.name = kwargs.get('name', 'CronTab ({0})'.format(id(self)))
        self.daemon = True
        self.jobs = {}
        self.proc_event = threading.Event()
        self.stop_event = threading.Event()

    def register(self, name, job):
        self.jobs[name] = job
        self.proc_event.set()

    def deregister(self, name):
        if name in self.jobs:
            del self.jobs[name]
            if len(self.jobs) == 0:
                self.proc_event.clear()

    def stop(self):
        self.stop_event.set()
        self.proc_event.clear()

    def run(self):
        LOG.debug('{0} started.'.format(self.name))
        try:
            while True:
                self.proc_event.wait()
                if self.stop_event.is_set():
                    LOG.info('{0} stopped.'.format(self.name))
                    return

                now = datetime.datetime.now()
                for _, job in self.jobs.items():
                    if now in job.cron:
                        threading.Thread(target=job).start()

                time.sleep(1)
        except Exception:
            LOG.exception('{0} encountered unhandled exception. '.format(self.name))

tab = CronTab()

def job(*args, **kwargs):
    ctab = kwargs.pop('tab', tab)
    on_success = kwargs.pop('on_success', lambda ctx: None)
    on_failure = kwargs.pop('on_failure', lambda ctx: None)
    cron = CronExpression(**kwargs)
    fargs = dict((k, kwargs[k]) for k in kwargs.keys() if k not in CronExpression.FIELD_NAMES) #func specific kwargs

    def decorator(func):
        @functools.wraps(func)
        def f():
            try:
                return on_success(func(*args, **fargs))
            except Exception as e:
                return on_failure(e)
        f.cron = cron
        f.name = func.name = '.'.join((func.__module__ or '__main__', func.__name__))
        ctab.register(f.name, f)
        return f
    return decorator
