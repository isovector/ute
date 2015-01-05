import datetime, time

def now():
    return time.time()

def morningOf(stamp):
    return time.mktime(
        datetime.datetime.fromtimestamp(stamp).date().timetuple())

