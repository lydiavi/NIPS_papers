from abc import ABC, abstractmethod
from typing import List

import pandas as pd


class DataLoader(ABC):
    """Abstract class for NIPS Paper Loading."""

    @abstractmethod
    def read_filter_data(self, years: List[int] | None) -> dict[str, pd.DataFrame]:
        """Read and filter NIPS Paper.

        Args:
            years (List[int]): list of years to keep

        Returns:
            dict[str, pd.DataFrame]: Dict with three elements : "papers", "authors" and "paper_authors"
        """
        pass

    def check_data_integrity(self, df: pd.DataFrame) -> None:
        """Removing lines with full nas, checking for unique id.

        Args:
            df (pd.DataFrame): DataFrame containing at least "id" column

        Raises:
            Exception: If id isn't unique, raises error
        """
        df.dropna(how="all", inplace=True)
        if not df["id"].is_unique:
            raise Exception("Id is not unique")

    def check_data_schema(self, data_col, expected_col) -> None:
        """Checking wether received columns match expected columns.

        Args:
            data_col (_type_): received columns
            expected_col (_type_): expected columns

        Raises:
            Exception: _description_
        """
        if not all(col in expected_col for col in data_col):
            raise Exception(
                f"Expected column missing from file. Expected {expected_col} received {data_col}"
            )
