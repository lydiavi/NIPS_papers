import os
from typing import List

import pandas as pd

from src.dataloader.const import (
    EXPECTED_COL_AUTHORS,
    EXPECTED_COL_PAPER_AUTHORS,
    EXPECTED_COL_PAPERS,
)
from src.dataloader.data_loader import DataLoader


class CSVLoader(DataLoader):
    """Load NIPS Paper in CSV format."""

    def __init__(self, path_to_files: str) -> None:
        self.path_to_files: str = path_to_files

    def read_filter_data(self, years: List[int] | None = None) -> dict[str, pd.DataFrame]:
        """Read CSV and filter according to years. Verification on data schema and unique key.

        Args:
            years (List[int]): list of years to keep

        Returns:
            dict[str, pd.DataFrame]: Dict with three elements : "papers", "authors" and "paper_authors"
        """
        # TODO : change path ?
        authors_df = pd.read_csv(os.path.join(self.path_to_files, "authors.csv"), encoding="utf-8")
        paper_authors_df = pd.read_csv(
            os.path.join(self.path_to_files, "paper_authors.csv"), encoding="utf-8"
        )
        papers_df = pd.read_csv(os.path.join(self.path_to_files, "papers.csv"), encoding="utf-8")

        self.check_data_schema(authors_df.columns, EXPECTED_COL_AUTHORS)
        self.check_data_schema(paper_authors_df.columns, EXPECTED_COL_PAPER_AUTHORS)
        self.check_data_schema(papers_df.columns, EXPECTED_COL_PAPERS)

        self.check_data_integrity(authors_df)
        self.check_data_integrity(paper_authors_df)
        self.check_data_integrity(papers_df)
        # TODO Filter in seperate func ?
        if years:
            papers_df = papers_df.loc[papers_df["year"].isin(years)]

            paper_ids_to_keep = papers_df["id"].unique()
            paper_authors_df = paper_authors_df[
                paper_authors_df["paper_id"].isin(paper_ids_to_keep)
            ]

            author_ids_to_keep = paper_authors_df["author_id"].unique()
            authors_df = authors_df[authors_df["id"].isin(author_ids_to_keep)]

        return {"authors": authors_df, "paper_authors": paper_authors_df, "papers": papers_df}
