# Most of this code is based on the LangChain's "Build a Question/Answering system over
# SQL data" tutorial available at https://python.langchain.com/docs/tutorials/sql_qa/.

from typing import Dict

from langchain import chat_models, hub
from langchain_community import tools, utilities
from langgraph import graph
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


class Agent:

    def __init__(self, db_uri: str, model: str, model_provider: str):
        self._db = utilities.SQLDatabase.from_uri(db_uri)
        self._llm = chat_models.init_chat_model(model, model_provider=model_provider)
        self._query_prompt_template = hub.pull("langchain-ai/sql-query-system-prompt")

        graph_builder = graph.StateGraph(State).add_sequence(
            [self._write_query, self._execute_query, self._generate_answer]
        )
        graph_builder.add_edge(graph.START, "_write_query")
        self._compiled_graph = graph_builder.compile()

    def _write_query(self, state: State) -> Dict[str, str]:
        """
        Generate SQL query to fetch information.
        """
        prompt = self._query_prompt_template.invoke(
            {
                "dialect": self._db.dialect,
                "top_k": 10,
                "table_info": self._db.get_table_info(),
                "input": state["question"],
            }
        )
        structured_llm = self._llm.with_structured_output(QueryOutput)
        return {"query": structured_llm.invoke(prompt)["query"]}

    def _execute_query(self, state: State) -> Dict[str, str]:
        """
        Execute SQL query.
        """
        execute_query_tool = tools.QuerySQLDatabaseTool(db=self._db)
        return {"result": execute_query_tool.invoke(state["query"])}

    def _generate_answer(self, state: State) -> Dict[str, str]:
        """
        Answer question using retrieved information as context.
        """
        prompt = (
            "Given the following user question, corresponding SQL query, "
            "and SQL result, answer the user question.\n\n"
            f'Question: {state["question"]}\n'
            f'SQL Query: {state["query"]}\n'
            f'SQL Result: {state["result"]}'
        )
        return {"answer": self._llm.invoke(prompt).content}

    def run(self, question: str):
        """
        Run the steps in a single sequence.
        """
        print(f"\nQUESTION:\n{question}\n")

        for step in self._compiled_graph.stream(
            {"question": question}, stream_mode="updates"
        ):
            for step_key, step_value in step.items():
                for state, state_value in step_value.items():
                    print(f"- {state}:\n{state_value}")
