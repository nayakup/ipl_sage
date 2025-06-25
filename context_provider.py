from atomic_agents.lib.components.system_prompt_generator import SystemPromptContextProviderBase

from config import MatchData, get_logger
from services.preprocess import PreprocessIPLData

logger = get_logger(__name__)


class IPLContextProvider(SystemPromptContextProviderBase):
    """Provide IPL Data Schema as context"""

    def __init__(self, title: str):
        super().__init__(title=title)

    def get_info(self) -> str:
        return self.generate_schema_description_duckdb()

    def generate_schema_description_duckdb(self) -> str:
        """

        Generate a human-readable schema description of the DuckDB table.

        Returns:
            str: Schema description with table info and sample data.

        """
        # Read CSV and Load to DuckDB, return connection, database name and table name
        preprocess = PreprocessIPLData()
        self.connection = preprocess.connection

        # Get Schema for CSVs
        schema = MatchData.model_json_schema()

        ###### Generate Context BEGIN ############
        description_lines = [
            f"The DuckDB table '{preprocess.table_name}' contains IPL match data with the following columns:\n"
        ]

        for field_name, field_info in schema.get("properties", {}).items():
            field_type = field_info.get("type", "unknown")
            desc = field_info.get("description", "No description available")
            description_lines.append(f"- {field_name} ({field_type}): {desc}")

        row_count = preprocess.connection.execute(f"SELECT COUNT(*) FROM {preprocess.table_name}").fetchone()[0]  # noqa: S608
        col_count = len(preprocess.connection.execute(f"PRAGMA table_info('{preprocess.table_name}')").fetchall())
        description_lines.append(f"\nTable shape: ({row_count} rows, {col_count} columns)")

        sample_df = preprocess.connection.execute(f"SELECT * FROM {preprocess.table_name} LIMIT 3").fetchdf()  # noqa: S608
        description_lines.append(f"\nSample data:\n{sample_df.to_string(index=False)}")
        logger.info("Generated schema description")
        ###### Generate Context END ############
        return "\n".join(description_lines)
