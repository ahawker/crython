"""
    crython/tab
    ~~~~~~~~~~~

    Contains functionality for executing jobs (python functions) from cron expressions.
"""

import datetime
import threading
import multiprocessing
import time

from crython.log import LOG


__all__ = ['CronTab', 'default_tab', 'start', 'stop']


#: Mapping of supported execution contexts for registered jobs.
EXECUTION_CONTEXTS = {
    'thread': lambda job: threading.Thread(target=job).start(),
    'multiprocess': lambda job: multiprocessing.Process(target=job).start(),
}


class CronTab(threading.Thread):
    """
    Background thread responsible for executing background jobs.
    """

    def __init__(self, *args, **kwargs):
        super(CronTab, self).__init__(*args, **kwargs)
        self.name = 'CronTab ({0})'.format(kwargs.get('name', id(self)))
        self.daemon = True
        self.jobs = {}
        self.jobs_lock = threading.RLock()
        self.proc_event = threading.Event()
        self.stop_event = threading.Event()

    def register(self, name, job):
        """
        Register the given name and function.

        :param name: Name of the registered job. **Note:** This should be unique.
        :param job: Callable decorated with :func:`~crython.job.job` to execute.
        :return: `None`.
        """
        with self.jobs_lock:
            self.jobs[name] = job
            self.proc_event.set()

    def deregister(self, name):
        """
        De-register the job that was registered with the given name.

        :param name: Name of the job to remove.
        :return: `None`.
        """
        with self.jobs_lock:
            if name in self.jobs:
                del self.jobs[name]
                if not len(self.jobs):
                    self.proc_event.clear()

    def stop(self):
        """
        Stop this background thread from executing any more jobs.

        :return: `None`.
        """
        with self.jobs_lock:
            self.stop_event.set()
            self.proc_event.clear()
            self.jobs.clear()

    def run(self):
        """
        Background function that processes all registered jobs and invokes them based on their context and expression.
        """
        LOG.info('{0} started'.format(self.name))
        try:
            # Wait until there is at least one registered job. No point is spinning otherwise.
            self.proc_event.wait()

            # Pop and execute any jobs that should be run at "reboot". Reboot, in this context, is just whenever
            # the executor starts running.
            for job in (self.jobs.pop(k) for (k, v) in self.jobs.items() if v.cron_expression.is_reboot):
                EXECUTION_CONTEXTS[job.ctx](job)

            # Spin loop.
            # TODO - This can be infinitely more efficient if we convert cron expressions to a
            # datetime/timedelta so we know exactly how long we should sleep before waking up to execute.
            while True:
                self.proc_event.wait()
                if self.stop_event.is_set():
                    LOG.info('{0} stopped'.format(self.name))
                    break

                now = datetime.datetime.now()
                for _, job in self.jobs.copy().items():
                    if now in job.cron:
                        EXECUTION_CONTEXTS[job.ctx](job)

                time.sleep(1)
        except Exception:
            LOG.exception('{0} encountered unhandled exception'.format(self.name))
        finally:
            LOG.info('{0} exiting'.format(self.name))


#: The default, global tab instance that is created on import. This is the instance that will be used unless
#: the :func:`~crython.job.job` caller overrides it.
default_tab = CronTab(name='default')


def start():
    """
    Start the default, global :class:`~crython.tab.CronTab` instance.
    """
    global default_tab

    default_tab.start()


def stop():
    """
    Stop the default, global :class:`~crython.tab.CronTab` instance.
    """
    global default_tab

    default_tab.stop()
