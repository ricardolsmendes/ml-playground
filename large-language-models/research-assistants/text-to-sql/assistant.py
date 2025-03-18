# Most of this code is based on the LangChain's "Build a Question/Answering system over
# SQL data" tutorial available at https://python.langchain.com/docs/tutorials/sql_qa/.

from typing import Dict

from langchain import chat_models
from langchain_community import utilities
from langgraph import graph

import agents
from agents import State


class Assistant:

    def __init__(self, db_uri: str, model: str, model_provider: str):
        self._db = utilities.SQLDatabase.from_uri(db_uri)
        self._llm = chat_models.init_chat_model(model, model_provider=model_provider)

        self._write_query_agent = agents.WriteQueryAgent()

        graph_builder = graph.StateGraph(State).add_sequence(
            [self._write_query, self._execute_query, self._generate_answer]
        )
        graph_builder.add_edge(graph.START, "_write_query")
        self._compiled_graph = graph_builder.compile()

    def _write_query(self, state: State) -> Dict[str, str]:
        return self._write_query_agent.run(self._db, state, self._llm)

    def _execute_query(self, state: State) -> Dict[str, str]:
        return agents.ExecuteQueryAgent.run(self._db, state)

    def _generate_answer(self, state: State) -> Dict[str, str]:
        return agents.GenerateAnswerAgent.run(state, self._llm)

    def run(self, question: str):
        """
        Run the steps in a single sequence.
        """
        print(f"\nQUESTION:\n{question}\n")

        steps = self._compiled_graph.stream(
            {"question": question}, stream_mode="updates"
        )

        for step in steps:
            for _, state in step.items():
                for key, value in state.items():
                    print(f"- {key}:\n{value}")
