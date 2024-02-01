from typing import List

import pandas as pd
from loguru import logger

from src.models.quickbook import QuickBook
from src.settings import CREDENTIALS
from src.utils.common_utils import get_last_day_of_month


def get_new_token_from_refresh_token(qb: QuickBook):
    new_token = qb.refresh_access_token(CREDENTIALS["refresh_token"])
    return new_token.get("access_token", None)


def get_profit_and_loss_df(
    qb: QuickBook,
    start_date: str,
    end_date: str,
    account_method: List[str],
    summarize_column_by: str = "Month",
    minorversion: int = 70,
):
    df = pd.DataFrame()
    for method in account_method:
        logger.info(f"get_profit_and_loss of account_method {method}")
        result = qb.get_profit_and_loss(
            start_date=start_date,
            end_date=end_date,
            account_method=method,
            summarize_column_by=summarize_column_by,
            minorversion=minorversion,
        )
        res_df = qb.convert_response_to_df(result)
        df = pd.concat([df, res_df], axis=0)
    return df


def get_balance_sheet_df(
    qb: QuickBook,
    start_date: str,
    end_date: str,
    account_method: List[str],
    summarize_column_by: str = "Month",
    minorversion: int = 70,
):
    df = pd.DataFrame()
    for method in account_method:
        logger.info(f"get_balance_sheet of account_method {method}")
        result = qb.get_balance_sheet(
            start_date=start_date,
            end_date=end_date,
            account_method=method,
            summarize_column_by=summarize_column_by,
            minorversion=minorversion,
        )
        res_df = qb.convert_response_to_df(result)
        df = pd.concat([df, res_df], axis=0)
    return df


def get_cash_flow_df(
    qb: QuickBook,
    start_date: str,
    end_date: str,
    summarize_column_by: str = "Month",
    minorversion: int = 70,
):
    result = qb.get_cash_flow(
        start_date=start_date,
        end_date=end_date,
        summarize_column_by=summarize_column_by,
        minorversion=minorversion,
    )
    res_df = qb.convert_response_to_df(result)
    return res_df


if __name__ == "__main__":
    qb = QuickBook.get_connection(credentials=CREDENTIALS)

    # choose start_date (%y-%m-%d)
    start_date = "2023-08-01"
    last_day_of_month = get_last_day_of_month().strftime("%Y-%m-%d")
    end_date = last_day_of_month
    account_method = ["Cash", "Accrual"]
    summarize_column_by = ["Total", "Month", "Week", "Days", "Quarter", "Year"]

    # you can get info following summarize_column_by, default is 'Month'
    # get data of balance_sheet
    bs_df = get_balance_sheet_df(
        qb=qb,
        start_date=start_date,
        end_date=end_date,
        account_method=account_method,
        summarize_column_by="Month",
    )
    print(bs_df.head(5))
    qb.save_df_to_gpq(
        bs_df,
        project_id="radar-377104",
        dataset_id="api_connection",
        table_id="quickbook_balance_sheet",
        if_exists="replace",
    )

    # get data of profit_and_loss
    # pl_df = get_profit_and_loss_df(
    #     qb=qb,
    #     start_date=start_date,
    #     end_date=end_date,
    #     account_method=account_method,
    #     summarize_column_by="Month",
    # )
    # print(pl_df.head(5))
    # qb.save_df_to_gpq(
    #     pl_df,
    #     project_id="radar-377104",
    #     dataset_id="api_connection",
    #     table_id="quickbook_profit_and_loss",
    #     if_exists="replace"
    # )

    # # get data of cash_flow
    # cf_df = get_cash_flow_df(
    #     qb=qb,
    #     start_date=start_date,
    #     end_date=end_date,
    #     summarize_column_by="Month",
    # )
    # print(cf_df.head(5))
    # qb.save_df_to_gpq(
    #     cf_df,
    #     project_id="radar-377104",
    #     dataset_id="api_connection",
    #     table_id="quickbook_cash_flowwww",
    #     if_exists="replace"
    # )
