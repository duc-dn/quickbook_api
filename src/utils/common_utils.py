import calendar
import datetime


def get_last_day_of_month():
    # Get the current year and month
    current_year = datetime.datetime.now().year
    current_month = datetime.datetime.now().month

    # Get the last day of the current month
    last_day = calendar.monthrange(current_year, current_month)[1]

    # Create a datetime object for the last day of the current month
    last_date_of_month = datetime.datetime(current_year, current_month, last_day)
    return last_date_of_month
