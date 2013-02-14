# crython [![Build Status](https://travis-ci.org/ahawker/crython.png)](https://travis-ci.org/ahawker/crython)
crython is a python implementation of [cron](http://en.wikipedia.org/wiki/Cron) which can schedule tasks (functions) from standard cron expressions or python objects.

### Status
This module is currently under development.

### Usage

Crython supports seven fields (seconds, minutes, hours, day of month, month, weekday, year).  
Call a function once a second:::

    import crython
    
    #Fire once a minute.
    crython.job(minute=0)
    def foo():
        print "... while heavy sack beatings are up a shocking nine hundred percent?"
        
Call a function every ten seconds:::

    #Fire every 10 seconds.
    crython.job(second=range(0,60,10))
    def foo():
        print "I'm a big four-eyed lame-o and I wear the same stupid sweater every day."
        
Call functions with a full cron expression:::

    #Fire once a week.
    crython.job(expr='0 0 0 * * 0 *')
    def foo():
        print "Back in line, maggot!"

Call functions with arguments:::

    #Fire every second.
    crython.job(second=0)
    def sum(x, y):
        print 'Sum={0}'.format(x + y)

Start the global job scheduler:::
    
    if __name__ == '__main__':
        crython.tab.start()

### Contributing
If you would like to contribute, simply fork the repository, push your changes and send a pull request.

### License
Crython is available under the [MIT license](https://github.com/ahawker/crython/blob/master/license.md).

### See Other
There are other python implementations of cron out there.
See: [pycron](http://www.kalab.com/freeware/pycron/pycron.htm), [python-crontab](http://pypi.python.org/pypi/python-crontab/).