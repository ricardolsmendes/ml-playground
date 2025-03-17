from typing import Mapping

from langchain import chat_models

from postgres_helper import DatabaseHelper


class TableMetadataEnrichmentAgent:

    def __init__(self, db_helper: DatabaseHelper):
        self._db_helper = db_helper
        self._llm = chat_models.init_chat_model("gpt-4o-mini", model_provider="openai")

    def _generate_description(self, table_info, sample_data) -> Mapping[str, str]:
        prompt = (
            "Given the following rules, table information and sample data,"
            " provide a human-friendly description for the table."
            "\n\n"
            "Rules:\n"
            "1. Do not include any column description in the answer.\n"
            "2. Do not include any sensitive information in the answer.\n"
            "3. Include 3 examples of data from the table in the answer.\n"
            "\n\n"
            f"Table info: {table_info}"
            f"\n\n"
            f"Sample data: {sample_data}"
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

            plain_text_table_info = [
                ", ".join([f"{col}: {row[col]}" for col in table_info.columns])
                for _, row in table_info.iterrows()
            ]
            plain_text_sample_data = [
                ", ".join([f"{col}: {row[col]}" for col in sample_data.columns])
                for _, row in sample_data.iterrows()
            ]

            description = self._generate_description(
                plain_text_table_info, plain_text_sample_data
            ).get("answer")

            print(
                f"\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
                f"\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
                f"Table: {table}\n\n"
                f"Description: {description}\n"
                f"\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
                f"\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
            )

            self._db_helper.set_table_description(schema, table, description)
