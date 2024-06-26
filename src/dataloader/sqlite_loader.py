import os
import sqlite3
from typing import List

import pandas as pd

from src.dataloader.const import (
    EXPECTED_COL_AUTHORS,
    EXPECTED_COL_PAPER_AUTHORS,
    EXPECTED_COL_PAPERS,
)
from src.dataloader.data_loader import DataLoader


class SQLITELoader(DataLoader):
    """Load NIPS Paper from Sqlite Database."""

    def __init__(self, path_to_files: str) -> None:
        self.path_to_files: str = path_to_files

    def read_filter_data(self, years: List[int] | None = None) -> dict[str, pd.DataFrame]:
        """Read from SQLite Database and filter according to years. Verification on data schema and unique key.

        Args:
            years (List[int]): list of years to keep

        Returns:
            dict[str, pd.DataFrame]: Dict with three elements : "papers", "authors" and "paper_authors"
        """
        # TODO: think of a better way to use db, having it return the same as csv might not be optimal
        connect = sqlite3.connect(os.path.join(self.path_to_files, "database.sqlite"))
        query_pa_authors = """
        SELECT *
        FROM paper_authors JOIN papers ON paper_authors.paper_id = papers.id
        JOIN authors ON paper_authors.author_id = authors.id
        """

        if years:
            query_pa_authors += f"""
            WHERE papers.Year IN ({",".join([str(y) for y in years])})"""

        all_df = pd.read_sql(query_pa_authors, connect)

        authors_df = all_df.iloc[:, 10:].drop_duplicates()
        paper_authors_df = all_df.iloc[:, :3].drop_duplicates()
        papers_df = all_df.iloc[:, 3:10].drop_duplicates()

        self.check_data_schema(authors_df.columns, EXPECTED_COL_AUTHORS)
        self.check_data_schema(paper_authors_df.columns, EXPECTED_COL_PAPER_AUTHORS)
        self.check_data_schema(papers_df.columns, EXPECTED_COL_PAPERS)

        self.check_data_integrity(authors_df)
        self.check_data_integrity(paper_authors_df)
        self.check_data_integrity(papers_df)
        return {"authors": authors_df, "paper_authors": paper_authors_df, "papers": papers_df}
