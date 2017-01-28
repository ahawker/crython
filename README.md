# crython

[![Join the chat at https://gitter.im/crython/Lobby](https://badges.gitter.im/crython/Lobby.svg)](https://gitter.im/crython/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

[![PyPI version](https://badge.fury.io/py/crython.svg)](https://badge.fury.io/py/crython)
[![PyPI versions](https://img.shields.io/pypi/pyversions/crython.svg)](https://pypi.python.org/pypi/crython)
[![PyPI downloads](https://img.shields.io/pypi/dm/crython.svg)](https://pypi.python.org/pypi/crython)
[![Build Status](https://travis-ci.org/ahawker/crython.png)](https://travis-ci.org/ahawker/crython)
[![Coverage Status](https://coveralls.io/repos/ahawker/crython/badge.png?branch=master)](https://coveralls.io/r/ahawker/crython)
[![Stories in Ready](https://badge.waffle.io/ahawker/crython.svg?label=ready&title=Ready)](http://waffle.io/ahawker/crython)
[![Code Climate](https://codeclimate.com/github/ahawker/crython/badges/gpa.svg)](https://codeclimate.com/github/ahawker/crython)
[![Issue Count](https://codeclimate.com/github/ahawker/crython/badges/issue_count.svg)](https://codeclimate.com/github/ahawker/crython)

crython is a lightweight task (function) scheduler using [cron](http://en.wikipedia.org/wiki/Cron) expressions written in python.

### Status
This module is currently under development.

### Installation
To install crython from [pip](https://pypi.python.org/pypi/pip):
```bash
    $ pip install crython
```

To install crython from source:
```bash
    $ git clone git@github.com:ahawker/crython.git
    $ python setup.py install
```

### Usage
Crython supports seven fields (seconds, minutes, hours, day of month, month, weekday, year).

Call a function once a minute:
```python
    import crython
    
    #Fire once a minute.
    @crython.job(second=0)
    def foo():
        print "... while heavy sack beatings are up a shocking nine hundred percent? - Kent Brockman"
```
        
Call a function every ten seconds:  
```python
    #Fire every 10 seconds.
    @crython.job(second=range(0,60,10))
    def foo():
        print "I'm a big four-eyed lame-o and I wear the same stupid sweater every day. - Homer's Brain"
```

Call a function with a single cron expression:
```python
    #Fire every 10 seconds.
    @crython.job(second='*/10')
    def foo():
        print "Hail to the thee Kamp Krusty... - Kampers"
```
        
Call a function with a full cron expression:
```python
    #Fire once a week.
    @crython.job(expr='0 0 0 * * 0 *')
    def foo():
        print "Back in line, maggot! - Kearny"
```

Call a function with positional and/or keyword arguments:
```python
    #Fire every second.
    @job('safety gloves', second='*', name='Homer Simpson')
    def foo(item, name):
        print "Well, I don't need {0}, because I'm {1}. -- Grimey".format(item, name)
```

Call a function using [predefined keywords](https://github.com/ahawker/crython#keywords):
```python
    #Fire once a day.
    @crython.job(expr='@daily')
    def foo():
        print "That's where I saw the leprechaun. He tells me to burn things! - Ralph Wiggum"
```

```python
    #Fire once immediately after scheduler starts.
    @crython.job(expr='@reboot')
    def foo():
        print "I call the big one bitey. - Homer Simpson"
```

Call a function and run it within a separate process:
```python
    #Fire every hour.
    @crython.job(expr='@hourly', ctx='process')
    def foo():
        print "No, no, dig up stupid. - Chief Wiggum"
```

Start the global job scheduler:  
```python
    if __name__ == '__main__':
        crython.tab.run()
```

### Keywords
| Entry | Description | Equivalent To |
| --- | --- | --- |
| @yearly/@annually | Run once a year at midnight in the morning of January 1 | 0 0 0 0 1 1 * |
| @monthly | Run once a month at midnight in the morning of the first of the month | 0 0 0 0 1 * * |
| @weekly | Run once a week at midnight in the morning of Sunday | 0 0 0 0 * 0 * |
| @daily | Run once a day at midnight | 0 0 0 * * * * |
| @hourly | Run once an hour at the beginning of the hour | 0 0 * * * * * |
| @minutely | Run once a minute at the beginning of the minute | 0 * * * * * * |
| @reboot | Run once at startup | @reboot |

### TODO
- Support "L", "W" and "#" specials.
- Determine time delta from now -> next time expression is valid.

### Contributing
If you would like to contribute, simply fork the repository, push your changes and send a pull request.

### License
Crython is available under the [MIT license](https://github.com/ahawker/crython/blob/master/LICENSE.md).

### See Other
There are similar python cron libraries out there.
See:
[pycron](http://www.kalab.com/freeware/pycron/pycron.htm),
[python-crontab](http://pypi.python.org/pypi/python-crontab/),
[cronex](https://github.com/jameseric/cronex).
