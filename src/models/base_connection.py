import asyncio
from abc import ABC, abstractmethod
from typing import Dict

from pandas import DataFrame


class BaseConnection(ABC):
    CONNECTION_NAME = "base"
    CRED_TYPE = None

    @abstractmethod
    def __init__(self):
        pass

    @classmethod
    def get_connection(cls, credentials: Dict):
        """
        Get instance of class
        Args:
            credentials:

        Returns:

        """
        pass

    # @abstractmethod
    @classmethod
    def get_connection_name(cls) -> str:
        return cls.CONNECTION_NAME

    @staticmethod
    def save_df_to_csv(df: DataFrame, file_name: str, target_folder: str) -> None:
        df.to_csv(f"{target_folder}/{file_name}")
