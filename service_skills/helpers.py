import datetime


def now():
    return datetime.datetime.utcnow()


def nowf():
    return now().isoformat()
