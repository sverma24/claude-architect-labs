from datetime import datetime


def now():
    return datetime.utcnow()


def format_day(value):
    """Turn a datetime into '21 Oct 2026' for receipts."""
    return value.strftime("%d %b %Y")


def days_between(start, end):
    return (end - start).days
