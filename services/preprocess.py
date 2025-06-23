import re
from pathlib import Path

import duckdb

from config import DATABASE_NAME, DATABASE_TABLE, MatchData, get_logger

logger = get_logger(__name__)


class PreprocessIPLData:
    def __init__(self, table_name: str = DATABASE_TABLE, db_name: str = DATABASE_NAME):
        self.table_name = table_name
        self.db_name = db_name
        self.connection = self.process_duckdb_table(recreate_table=False)

    def is_safe_table_name(self, name: str) -> bool:
        return re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", name) is not None

    def process_duckdb_table(self, file_dir: str = Path(__file__).parent, *, recreate_table: bool = False):
        """
        Process CSV files with DuckDB and create or refresh the table.

        Args:
            file_dir: Directory containing CSV files.
            recreate_table: If True, drop and recreate the table.

        Returns:
            duckdb.DuckDBPyConnection: Connection with processed data.

        """
        db_path = Path(file_dir) / self.db_name
        con = duckdb.connect(database=db_path)
        logger.info("Connected to DuckDB database at %s", db_path)

        if recreate_table:
            logger.info("Recreating table...")
            if not self.is_safe_table_name(self.table_name):
                msg = f"Unsafe table name: {self.table_name}"
                logger.error(msg)
                raise ValueError(msg)

            csv_files = [str(p) for p in Path(file_dir).glob("*.csv")]
            if not csv_files:
                msg = f"No CSV files found in directory: {file_dir}"
                logger.error(msg)
                raise FileNotFoundError(msg)

            con.execute(f"DROP TABLE IF EXISTS {self.table_name}")
            logger.info("Dropped existing table %s (if any)", self.table_name)

            con.execute(
                f"""
                CREATE TABLE {self.table_name} AS
                SELECT * FROM read_csv_auto(?, union_by_name=True)
                """,  # noqa: S608
                [csv_files],
            )
            logger.info("Created table %s from CSV files", self.table_name)

        self.connection = con
        return con

    def generate_schema_description_duckdb(self) -> str:
        """

        Generate a human-readable schema description of the DuckDB table.

        Returns:
            str: Schema description with table info and sample data.

        """
        schema = MatchData.model_json_schema()
        description_lines = [
            f"The DuckDB table '{DATABASE_TABLE}' contains IPL match data with the following columns:\n"
        ]

        for field_name, field_info in schema.get("properties", {}).items():
            field_type = field_info.get("type", "unknown")
            desc = field_info.get("description", "No description available")
            description_lines.append(f"- {field_name} ({field_type}): {desc}")

        row_count = self.connection.execute(f"SELECT COUNT(*) FROM {DATABASE_TABLE}").fetchone()[0]  # noqa: S608
        col_count = len(self.connection.execute(f"PRAGMA table_info('{DATABASE_TABLE}')").fetchall())
        description_lines.append(f"\nTable shape: ({row_count} rows, {col_count} columns)")

        sample_df = self.connection.execute(f"SELECT * FROM {DATABASE_TABLE} LIMIT 3").fetchdf()  # noqa: S608
        description_lines.append(f"\nSample data:\n{sample_df.to_string(index=False)}")

        logger.info("Generated schema description")
        return "\n".join(description_lines)


if __name__ == "__main__":
    preprocess = PreprocessIPLData()
    con = preprocess.process_duckdb_table(recreate_table=False)
    description = preprocess.generate_schema_description_duckdb()
    print(description)
