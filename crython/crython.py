import calendar
import os
import re
import datetime
import threading
import collections

__author__ = 'Andrew Hawker <andrew.r.hawker@gmail.com>'
__all__ = ['sec', 'min', 'hr', 'dom', 'mon', 'dow', 'yr']

#Keywords: #TODO
#@yearly (or @annually)	Run once a year at midnight in the morning of January 1     0 0 1 1 *
#@monthly   Run once a month at midnight in the morning of the first of the month   0 0 1 * *
#@weekly    Run once a week at midnight in the morning of Sunday                    0 0 * * 0
#@daily     Run once a day at midnight                                              0 0 * * *
#@hourly    Run once an hour at the beginning of the hour                           0 * * * *
#@reboot    Run at startup                                                          @reboot

SPECIALS = {'*', '/', '%', ',', '-', 'L', 'W', '#', '?'}

DAY_NAME = dict((v.lower(),k) for k,v in enumerate(calendar.day_name))      #(ex: Monday, Tuesday, etc)
DAY_ABBR = dict((v.lower(),k) for k,v in enumerate(calendar.day_abbr))      #(ex: Mon, Tue, etc)
MON_NAME = dict((v.lower(),k) for k,v in enumerate(calendar.month_name))    #(ex: January, February, etc)
MON_ABBR = dict((v.lower(),k) for k,v in enumerate(calendar.month_abbr))    #(ex: Jan, Feb, etc)
PHRASES  = dict(DAY_NAME.items() + DAY_ABBR.items() + MON_NAME.items() + MON_ABBR.items())
PHRASES_REGEX = re.compile('{0}'.format('|'.join(PHRASES.keys()).lstrip('|')), flags=re.IGNORECASE)

class CronField(collections.namedtuple('CronField', 'value min max specials')):
    def __new__(cls, *args, **kwargs):
        """
        Creates a new CronField from the given time by substituting english dow/mon phrases for their
        respective numeric values and validating string expressions for invalid special characters.
        """
        args = (CronField.sub_english_phrases(args[0]),) + args[1:]
        field = super(CronField, cls).__new__(cls, *args, **kwargs)
        if isinstance(field.value, basestring): #validate special characters for this field type
            invalid_chars = SPECIALS.difference(field.specials).intersection(set(field.value))
            if invalid_chars:
                raise ValueError('Found invalid characters: {0}'.format(','.join(invalid_chars)))
        return field

    def __contains__(self, item):
        """
        Determines if the given time is 'within' the time denoted by this individual field.
        """
        value = self.value
        if isinstance(value, (int, long)):
            return value == item
        if isinstance(value, basestring):
            result = False
            for value in re.split(r'[,]', value):               #comma separated values (ex: 1,4,10)
                value = re.split(r'[-/]', value)                #separate range and step characters
                if len(value) == 1:
                    if value[0] == '*':                         #single wildcard (ex: *)
                        return True
                    result |=  int(value[0]) == item            #single digit (ex: 10)
                if value[0] == '*':                             #wildcart w/ step (ex: */2 ==> 0-59/2)
                    value = [self.min, self.max, value[1]]
                start = int(value[0])                           #range (ex: 0-10)
                stop = int(value[1]) if len(value) > 1 else None
                step = int(value[2]) if len(value) > 2 else None    #range w/ step (ex: 0-10/2)
                result |= start <= item <= stop and (not step or (item + start) % step == 0)
            return result
        if isinstance(value, collections.Iterable):
            return item in value

    @staticmethod
    def sub_english_phrases(value):
        """
        Replace any full or abbreviated english dow/mon phrases (Jan, Monday, etc) from the field value
        with its respective integer representation.
        """
        def _repl(match):
            return str(PHRASES[match.group(0).lower()])
        return PHRASES_REGEX.sub(_repl, value)

sec = lambda *args,**kwargs: CronField(*(args + (0, 59,      {'*', '/', ',', '-'})),                **kwargs)
min = lambda *args,**kwargs: CronField(*(args + (0, 59,      {'*', '/', ',', '-'})),                **kwargs)
hr  = lambda *args,**kwargs: CronField(*(args + (0, 23,      {'*', '/', ',', '-'})),                **kwargs)
dom = lambda *args,**kwargs: CronField(*(args + (1, 31,      {'*', '/', ',', '-', '?', 'L', 'W'})), **kwargs)
mon = lambda *args,**kwargs: CronField(*(args + (1, 12,      {'*', '/', ',', '-'})),                **kwargs)
dow = lambda *args,**kwargs: CronField(*(args + (0, 6,       {'*', '/', '-', '?', 'L', '#'})),      **kwargs)
yr  = lambda *args,**kwargs: CronField(*(args + (1970, 2099, {'*', '/', ',', '-'})),                **kwargs)


CronTime = collections.namedtuple('CronTime', 'year month day hour minute second weekday')

class CronExpression(object):
    def __init__(self, second=None, minute=None, hour=None, day=None, month=None, weekday=None, year=None):
        self.second  = second  or sec('*')
        self.minute  = minute  or min('*')
        self.hour    = hour    or hr('*')
        self.day     = day     or dom('*')
        self.month   = month   or mon('*')
        self.weekday = weekday or dow('*')
        self.year    = year    or yr('*')

    def __contains__(self, item): #item should always be a datetime #XXX confirm and revise
        if not isinstance(item, datetime.datetime): #hrm
            return False
        item = CronTime(*item.timetuple()[:7])
        return all(getattr(item, k) in v for k,v in self.__dict__.items())

class CronJob(object):
    def __init__(self, cron, func, args, kwargs):
        self.cron = cron
        self.func = func
        self.args = args or ()
        self.kwargs = kwargs or {}

class CronTab(threading.Thread):
    pass