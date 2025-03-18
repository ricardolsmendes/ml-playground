from typing import List, Mapping
from typing_extensions import TypedDict

from langchain import chat_models
from langchain_core import prompts
from pandas import DataFrame

import prompt_templates


class State(TypedDict):
    table: str
    table_info: DataFrame
    sample_data: DataFrame
    description: str
    accepted: bool


class TableMetadataEnrichmentAgent:

    def __init__(self):
        self._llm = chat_models.init_chat_model("gpt-4o-mini", model_provider="openai")

    @classmethod
    def _convert_df_to_text(cls, df: DataFrame) -> List[str]:
        return [
            ", ".join([f"{col}: {row[col]}" for col in df.columns])
            for _, row in df.iterrows()
        ]

    def generate_description(self, state: State) -> Mapping[str, str]:
        prompt_template = prompts.ChatPromptTemplate.from_template(
            prompt_templates.TABLE_DESCRIPTION_SYSTEM_PROMPT
        )
        prompt_input = {
            "table_information": self._convert_df_to_text(state.get("table_info")),
            "sample_data": self._convert_df_to_text(state.get("sample_data")),
        }
        prompt = prompt_template.invoke(prompt_input)
        return {"description": self._llm.invoke(prompt).content}
