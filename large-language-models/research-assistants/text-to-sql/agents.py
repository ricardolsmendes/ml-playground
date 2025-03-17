# Most of this code is based on the LangChain's "Build a Question/Answering system over
# SQL data" tutorial available at https://python.langchain.com/docs/tutorials/sql_qa/.

from typing import Dict

from langchain import hub
from langchain.chat_models.base import BaseChatModel
from langchain_community import tools
from langchain_community.utilities.sql_database import SQLDatabase
from typing_extensions import Annotated, TypedDict


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


class WriteQueryAgent:

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
                "input": state["question"],
            }
        )
        structured_llm = llm.with_structured_output(QueryOutput)
        return {"query": structured_llm.invoke(prompt)["query"]}


class ExecuteQueryAgent:

    @classmethod
    def run(cls, db: SQLDatabase, state: State) -> Dict[str, str]:
        """
        Execute SQL query.
        """
        execute_query_tool = tools.QuerySQLDatabaseTool(db=db)
        return {"result": execute_query_tool.invoke(state["query"])}


class GenerateAnswerAgent:

    @classmethod
    def run(cls, state: State, llm: BaseChatModel) -> Dict[str, str]:
        """
        Answer question using retrieved information as context.
        """
        prompt = (
            "Given the following user question, corresponding SQL query,"
            " and SQL result, answer the user question."
            "\n\n"
            f"Question: {state['question']}\n"
            f"SQL Query: {state['query']}\n"
            f"SQL Result: {state['result']}"
        )
        return {"answer": llm.invoke(prompt).content}
