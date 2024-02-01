from enum import Enum


class AccountingMethod(str, Enum):
    """Accounting method for the transaction."""

    cash = "Cash"
    accrual = "Accrual"


class DateMacro(str, Enum):
    """Date macro for the transaction."""

    today = "Today"
    yesterday = "Yesterday"
    this_week = "This Week"
    last_week = "Last Week"
    this_week_to_date = "This Week-to-date"
    last_week_to_date = "Last Week-to-date"
    next_week = "Next Week"
    next_4_weeks = "Next 4 Weeks"
    next_month = "Next Month"
    this_fiscal_quarter = "This Fiscal Quarter"
    last_fiscal_quarter = "Last Fiscal Quarter"
    next_fiscal_quarter = "Next Fiscal Quarter"
    this_fiscal_year = "This Fiscal Year"
    last_fiscal_year = "Last Fiscal Year"
    this_fiscal_year_to_date = "This Fiscal Year-to-date"
    last_fiscal_year_to_date = "Last Fiscal Year-to-date"
    next_fiscal_year = "Next Fiscal Year"
