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

    @abstractmethod
    def check_data_integrity(self):
        """_summary_."""
        # TODO check for data quality problems like nas, unique ids, etc.
        # TODO remove decorator once done
        pass

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
