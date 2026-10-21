from datetime import datetime

from shop.utils.dates import days_between, format_day


def test_when_given_a_date_formats_day_month_year():
    # Arrange
    value = datetime(2026, 10, 21)
    # Act
    text = format_day(value)
    # Assert
    assert text == "21 Oct 2026"


def test_when_dates_are_a_week_apart_returns_seven():
    # Arrange
    start, end = datetime(2026, 10, 1), datetime(2026, 10, 8)
    # Act
    days = days_between(start, end)
    # Assert
    assert days == 7
