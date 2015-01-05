import datetime, time
import os, os.path

def now():
    return time.time()

def morningOf(stamp):
    return time.mktime(
        datetime.datetime.fromtimestamp(stamp).date().timetuple())

def homeDir(filename):
    return ("%s/%s" % (os.path.expanduser("~"), filename))
