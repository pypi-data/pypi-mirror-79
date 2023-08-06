from contextlib import contextmanager
from queue import Queue, Empty
import subprocess
from time import sleep
import threading


class CloudSQLProxy(threading.Thread):
    def __init__(self, command):
        self.command = command
        self.queue = Queue()
        threading.Thread.__init__(self)

    def run(self):
        self.process = subprocess.Popen(self.command.split(),
                                        shell=False,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)
        # The cloud_sql_proxy CLI write to stderr
        for line in iter(self.process.stderr.readline, b''):
            self.queue.put(line)
        self.process.stdout.close()


@contextmanager
def cloud_sql_proxy(connection_name):
    """A context manager to wrap a CLI call with a Cloud SQL Proxy connection.

    The execution will be blocked until the connection is ready to accept connections.
    The connection will be closed on exit.

    Use as a context manager:
    >>> with cloud_sql_proxy(connection_name='project:region:instance'):
    >>>     do_your_thing()

    """
    command = f'./cloud_sql_proxy -instances={connection_name} -dir=./cloudsql -verbose=false'
    proxy = CloudSQLProxy(command=command)
    proxy.start()

    try:
        while True:
            try:
                line = proxy.queue.get_nowait()
                if 'ready' in line.decode('utf-8').lower():
                    break  # Ready
            except Empty:
                pass  # Nothing yet
            sleep(2)
        yield proxy

    finally:
        proxy.process.terminate()
        proxy.join()


__all__ = ['cloud_sql_proxy']
