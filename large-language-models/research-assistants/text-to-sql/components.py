# Most of this code is based on the LangChain's "Build a Question/Answering system over
# SQL data" tutorial available at https://python.langchain.com/docs/tutorials/sql_qa/.

from typing import Dict

from langchain import hub
from langchain.chat_models.base import BaseChatModel
from langchain_community import tools
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_core import prompts
from typing_extensions import Annotated, TypedDict

import prompt_templates


class State(TypedDict):
    question: str
    query: str
    result: str
    answer: str


class QueryOutput(TypedDict):
    """
    Generated SQL query.
    """

    query: Annotated[str, ..., "Syntactically valid SQL query."]


class QueryGenerator:

    def __init__(self):
        # See https://smith.langchain.com/hub/langchain-ai/sql-query-system-prompt
        # for prompt details.
        self._query_prompt_template = hub.pull("langchain-ai/sql-query-system-prompt")

    def run(self, db: SQLDatabase, state: State, llm: BaseChatModel) -> Dict[str, str]:
        """
        Generate SQL query to fetch information.
        """
        prompt = self._query_prompt_template.invoke(
            {
                "dialect": db.dialect,
                "top_k": 10,
                "table_info": db.get_table_info(),
                "input": state.get("question"),
            }
        )
        structured_llm = llm.with_structured_output(QueryOutput)
        return {"query": structured_llm.invoke(prompt).get("query")}


class QueryExecutor:

    @classmethod
    def run(cls, db: SQLDatabase, state: State) -> Dict[str, str]:
        """
        Execute SQL query.
        """
        execute_query_tool = tools.QuerySQLDatabaseTool(db=db)
        return {"result": execute_query_tool.invoke(state.get("query"))}


class AnswerGenerator:

    @classmethod
    def run(cls, state: State, llm: BaseChatModel) -> Dict[str, str]:
        """
        Answer question using retrieved information as context.
        """
        prompt_template = prompts.ChatPromptTemplate.from_template(
            prompt_templates.SQL_ANSWER_SYSTEM_PROMPT
        )
        prompt_input = {
            "question": state.get("question"),
            "query": state.get("query"),
            "result": state.get("result"),
        }
        prompt = prompt_template.invoke(prompt_input)
        return {"answer": llm.invoke(prompt).content}
