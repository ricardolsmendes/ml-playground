from typing import List

from langchain import chat_models
from langchain_core import prompts
from pandas import DataFrame

from postgres_helper import DatabaseHelper
import prompt_templates


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
    ) -> str:
        generate_description_prompt_template = prompts.ChatPromptTemplate.from_template(
            prompt_templates.TABLE_DESCRIPTION_SYSTEM_PROMPT
        )
        prompt = generate_description_prompt_template.invoke(
            {
                "table_information": self._convert_data_frame_to_plain_text(table_info),
                "sample_data": self._convert_data_frame_to_plain_text(sample_data),
            }
        )
        return self._llm.invoke(prompt).content

    def run(self, schema: str) -> None:
        table_df = self._db_helper.list_tables(schema)
        tables = [row.table_name for row in table_df.itertuples()]
        for table in tables[:5]:
            table_info = self._db_helper.get_table_info(schema, table)
            sample_data = self._db_helper.get_sample_data(schema, table)
            description = self._generate_description(table_info, sample_data)

            print(f"Table: {table}\n\n" f"Description: {description}\n" f"\n\n")

            self._db_helper.set_table_description(schema, table, description)
