from threading import Thread
from time import sleep
import os

class LogReader(Thread):
    """
        Implements the logic to send day0 and day1 workflow's log to client.
    """
    def __init__(self, socketio, logfile):
        self.delay = 1
        super(LogReader, self).__init__()
        self.socketio = socketio
        self.logfile = logfile

    def tailf(self):
        """
            Reads logs from log file line by line.
            Sends each log line to client.
        """
        #os.chmod(self.logfile, 0666)
        def follow(thefile):
            """
                Reads newly added log lines in log files each second.
            """
            thefile.seek(0,2)      # Go to the end of the file
            while True:
                line = thefile.readline()
                if not line:
                    sleep(1)    # Sleep briefly
                    continue
                yield line

        thefile = open(self.logfile)
        loglines = follow(thefile)
        for line in loglines:
            self.socketio.emit('newline', line, namespace='/getlogs')

    def run(self):
        """
            Starts the thread.
        """
        self.tailf()
