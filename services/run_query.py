import pandas as pd

from services.preprocess import PreprocessIPLData


def run_duckdb_query(query: str) -> pd.DataFrame:
    """
    Execute a DuckDB SQL query and return the result as a pandas DataFrame.

    Args:
        query (str): SQL query string.

    Returns:
        pd.DataFrame: Query result as a DataFrame.

    """
    return PreprocessIPLData().connection.execute(query).fetchdf()


if __name__ == "__main__":
    pass
