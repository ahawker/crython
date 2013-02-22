# crython [![Build Status](https://travis-ci.org/ahawker/crython.png)](https://travis-ci.org/ahawker/crython)
crython is a lightweight task (function) scheduler using [cron](http://en.wikipedia.org/wiki/Cron) expressions written in python.

### Status
This module is currently under development.

### Usage
Crython supports seven fields (seconds, minutes, hours, day of month, month, weekday, year).

Call a function once a minute:
```python
    import crython
    
    #Fire once a minute.
    @crython.job(minute=0)
    def foo():
        print "... while heavy sack beatings are up a shocking nine hundred percent?"
```
        
Call a function every ten seconds:  
```python
    #Fire every 10 seconds.
    @crython.job(second=range(0,60,10))
    def foo():
        print "I'm a big four-eyed lame-o and I wear the same stupid sweater every day."
```

Call a function with a single cron expression:
```python
    #Fire every 10 seconds.
    @crython.job(second='*/10')
    def foo():
        print "Hail to the thee Kamp Krusty..."
```
        
Call functions with a full cron expression:  
```python
    #Fire once a week.
    @crython.job(expr='0 0 0 * * 0 *')
    def foo():
        print "Back in line, maggot!"
```

Call functions with positional and/or keyword arguments:  
```python
    #Fire every second.
    @crython.job(second=0, 10, 20, name='Homer Simpson')
    def sum(x, y, name):
        print "Hello {0}. The sum is {1}".format(name, x+y)
```

Start the global job scheduler:  
```python
    if __name__ == '__main__':
        crython.tab.start()
```

### TODO
- Keyword support (yearly, weekly, daily, etc)
- Support "L", "W" and "#" specials.
- Determine time delta from now -> next time expression is valid.

### Contributing
If you would like to contribute, simply fork the repository, push your changes and send a pull request.

### License
Crython is available under the [MIT license](https://github.com/ahawker/crython/blob/master/license.md).

### See Other
There are similar python cron libraries out there.
See: [pycron](http://www.kalab.com/freeware/pycron/pycron.htm),
[python-crontab](http://pypi.python.org/pypi/python-crontab/),
[cronex](https://github.com/jameseric/cronex).
