# crython [![Build Status](https://travis-ci.org/ahawker/crython.png)](https://travis-ci.org/ahawker/crython)
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

Call a function with [predefined keywords](http://en.wikipedia.org/wiki/Cron#Predefined_scheduling_definitions):
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

Start the global job scheduler:  
```python
    if __name__ == '__main__':
        crython.tab.start()
```

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
