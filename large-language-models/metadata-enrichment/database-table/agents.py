from typing import List, Mapping

from langchain import chat_models
from pandas import DataFrame

from postgres_helper import DatabaseHelper


class TableMetadataEnrichmentAgent:

    def __init__(self, db_helper: DatabaseHelper):
        self._db_helper = db_helper
        self._llm = chat_models.init_chat_model("gpt-4o-mini", model_provider="openai")

    @classmethod
    def _convert_data_frame_to_plain_text(cls, df: DataFrame) -> List[str]:
        return [
            ", ".join([f"{col}: {row[col]}" for col in df.columns])
            for _, row in df.iterrows()
        ]

    def _generate_description(
        self, table_info: DataFrame, sample_data: DataFrame
    ) -> Mapping[str, str]:
        prompt = (
            "Given the following rules, table information and sample data,"
            " provide a human-friendly description for the table."
            "\n\n"
            "Rules:\n"
            "1. Do not include any column description in the answer.\n"
            "2. Do not include any sensitive information in the answer.\n"
            "3. Include 3 examples of data from the table in the answer.\n"
            "\n\n"
            f"Table info: {self._convert_data_frame_to_plain_text(table_info)}"
            f"\n\n"
            f"Sample data: {self._convert_data_frame_to_plain_text(sample_data)}"
        )
        return {"answer": self._llm.invoke(prompt).content}

    def run(self, schema: str) -> None:
        table_df = self._db_helper.list_tables(schema)
        tables = [row.table_name for row in table_df.itertuples()]
        for table in [
            "airport",
            "country",
            "mergeswith",
            "geo_lake",
            "geo_mountain",
            "geo_estuary",
        ]:
            table_info = self._db_helper.get_table_info(schema, table)
            sample_data = self._db_helper.get_sample_data(schema, table)
            description = self._generate_description(table_info, sample_data).get(
                "answer"
            )

            print(
                f"Table: {table}\n\n"
                f"Description: {description}\n"
                f"\n\n"
            )

            self._db_helper.set_table_description(schema, table, description)
