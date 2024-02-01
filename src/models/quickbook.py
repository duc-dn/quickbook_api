import traceback
from typing import Any, Dict, Optional

import pandas as pd
import requests
from google.api_core.exceptions import Forbidden
from google.oauth2 import service_account
from loguru import logger

from src.models.base_connection import BaseConnection
from src.models.qbClient import AuthClient
from src.settings import BASE_URL, BIGQUERY_CREDETIALS, CLIENT_SECRET, CREDENTIALS


class QuickBook(BaseConnection):
    CONNECTION_NAME = "quickbook"
    CRED_TYPE = "json"
    BASE_URL = BASE_URL
    auth = AuthClient(**CLIENT_SECRET)

    def __init__(self, credentials: Dict):
        self.chunk_size = 1000
        self.realm_id = credentials["realm_id"]
        self.access_token = credentials["access_token"]
        self.refresh_token = credentials.get("refresh_token", None)

    def _send_http_request(self, url: str, method: str, payload: Any) -> dict:
        try:
            with open("./access_token.txt", "r") as f:
                access_token = f.read()
            if not access_token:
                access_token = self.access_token

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}",
            }
            response = requests.request(method, url, headers=headers, data=payload)

            if response.status_code == 401:
                # Access token expired, refresh and retry
                logger.warning("Access token expired. Refreshing token and retrying.")
                new_access_token = self.refresh_access_token(self.refresh_token)
                self.access_token = new_access_token["access_token"]
                with open("./access_token.txt", "w") as f:
                    f.write(self.access_token)

                headers["Authorization"] = f"Bearer {self.access_token}"
            response = requests.request(method, url, headers=headers, data=payload)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error("Failed to send HTTP request to QuickBook API")
            logger.error(traceback.format_exc())
            raise e

    def update_access_token(self, new_token):
        CREDENTIALS["access_token"] = new_token

    @classmethod
    def refresh_access_token(cls, refresh_token: str) -> str:
        response = cls.auth.refresh(refresh_token)
        return response

    @classmethod
    def get_connection(cls, credentials: Dict):
        instance = cls(credentials=credentials)
        return instance

    def get_profit_and_loss(
        self,
        start_date: str,
        end_date: str,
        account_method: str = "Cash",
        summarize_column_by: str = "Month",
        minorversion: int = 70,
    ):
        url = (
            f"{self.BASE_URL}/v3/company/{self.realm_id}/reports/ProfitAndLoss"
            f"?start_date={start_date}&end_date={end_date}&accounting_method={account_method}"
            f"&summarize_column_by={summarize_column_by}&minorversion={minorversion}"
        )
        payload = {}
        response = self._send_http_request(method="GET", url=url, payload=payload)
        logger.info(
            f"get_profit_and_loss of account_method {account_method} successfully"
        )
        return response

    def get_balance_sheet(
        self,
        start_date: str,
        end_date: str,
        account_method: str = "Cash",
        summarize_column_by: str = "Month",
        minorversion: int = 70,
    ):
        url = (
            f"{self.BASE_URL}/v3/company/{self.realm_id}/reports/BalanceSheet"
            f"?start_date={start_date}&end_date={end_date}&accounting_method={account_method}"
            f"&summarize_column_by={summarize_column_by}&minorversion={minorversion}"
        )
        payload = {}
        response = self._send_http_request(method="GET", url=url, payload=payload)
        logger.info("get_balance_sheet successfully")
        return response

    def get_cash_flow(
        self,
        start_date: str,
        end_date: str,
        summarize_column_by: str = "Month",
        minorversion: int = 70,
    ):
        url = (
            f"{self.BASE_URL}/v3/company/{self.realm_id}/reports/CashFlow"
            f"?start_date={start_date}&end_date={end_date}"
            f"&summarize_column_by={summarize_column_by}&minorversion={minorversion}"
        )
        payload = {}
        response = self._send_http_request(method="GET", url=url, payload=payload)
        return response

    @staticmethod
    def nomarlize_column_name(column_name: str):
        if len(column_name) == 0:
            return "Field"
        column_name = (
            column_name.strip().replace(" ", "").replace(",", " ").replace(" ", "_")
        )
        return column_name

    def extract_data_rows(self, row):
        data_rows = []
        if row.get("type") == "Data":
            data_rows.append(row["ColData"])
        if "Rows" in row:
            for sub_row in row["Rows"].get("Row", []):
                data_rows.extend(self.extract_data_rows(sub_row))
        return data_rows

    def get_list_rows(self, response: Dict):
        list_rows = []
        for r in response.get("Rows", {}).get("Row", []):
            list_rows.extend(self.extract_data_rows(r))

        row_lst = [[v.get("value") for v in row] for row in list_rows]
        return row_lst

    def get_list_columns(self, response: Dict):
        column_name_lst = []
        for col in response["Columns"]["Column"]:
            column_name_lst.append(self.nomarlize_column_name(col["ColTitle"]))
        return column_name_lst

    def convert_response_to_df(self, response: Dict):
        try:
            list_rows = self.get_list_rows(response)
            column_name_lst = self.get_list_columns(response)

            df = pd.DataFrame(data=list_rows, columns=column_name_lst)
            df = df.applymap(lambda x: 0 if x == "" else x)
            df[column_name_lst[1:]] = df[column_name_lst[1:]].astype("float")

            # get extra info from response
            extra_info = response.get("Header", {})
            extra_info.pop("Option")

            if extra_info:
                overlap_columns = set(column_name_lst) & set(extra_info.keys())

                if overlap_columns:
                    logger.warning(
                        f"Extra_info keys {overlap_columns} overlap with DataFrame columns."
                    )

                extra_df = pd.DataFrame([extra_info]).astype(str)
                df = pd.concat([extra_df, df], axis=1)
                df = df.ffill()
            else:
                logger.warning("Extra_info is empty.")
            logger.info(f"Convert response to df successfully")
            return df
        except Exception as e:
            logger.error(e)

    @staticmethod
    def save_df_to_gpq(
        df,
        project_id: str,
        dataset_id: str,
        table_id: str,
        if_exists: Optional[str] = "replace",
    ):
        try:
            table_name = f"{dataset_id}.{table_id}"
            credentials = service_account.Credentials.from_service_account_info(
                BIGQUERY_CREDETIALS
            )
            df.to_gbq(
                destination_table=table_name,
                project_id=project_id,
                credentials=credentials,
                if_exists=if_exists,
            )
            logger.info(f"Save to {table_name} successfully")
        except Forbidden as fe:
            logger.error(fe)
        except Exception as e:
            logger.error(e)
