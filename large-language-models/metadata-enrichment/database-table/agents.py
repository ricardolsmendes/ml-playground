from typing import Mapping
from typing_extensions import TypedDict

from langchain import chat_models
from langchain_core import prompts
from pandas import DataFrame

import prompt_templates


class State(TypedDict):
    table: str
    columns_technical_metadata: DataFrame
    sample_data: DataFrame
    description: str
    accepted: bool


class MetadataEnrichmentAgent:

    def __init__(self):
        self._llm = chat_models.init_chat_model("gpt-4o-mini", model_provider="openai")

    def generate_table_description(self, state: State) -> Mapping[str, str]:
        prompt_template = prompts.ChatPromptTemplate.from_template(
            prompt_templates.TABLE_DESCRIPTION_SYSTEM_PROMPT
        )
        prompt_input = {
            "columns_technical_metadata": state.get("columns_technical_metadata"),
            "sample_data": state.get("sample_data"),
        }
        prompt = prompt_template.invoke(prompt_input)
        return {"description": self._llm.invoke(prompt).content}


class ContentAcceptanceHelper:

    @classmethod
    def accept(cls) -> Mapping[str, bool]:
        return {"accepted": True}

    @classmethod
    def reject(cls) -> Mapping[str, bool]:
        return {"accepted": False}
