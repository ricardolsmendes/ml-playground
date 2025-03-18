from typing import Mapping, Optional

from langgraph import graph
from pandas import DataFrame

import agents
from agents import State


class MetadataEnrichmentAssistant:

    def __init__(self):
        self._table_metadata_enrichment_agent = agents.TableMetadataEnrichmentAgent()

        graph_builder = graph.StateGraph(State).add_sequence(
            [self._generate_table_description]
        )
        graph_builder.add_edge(graph.START, "_generate_table_description")
        self._compiled_graph = graph_builder.compile()

    def _generate_table_description(self, state: State) -> Mapping[str, str]:
        return self._table_metadata_enrichment_agent.generate_description(state)

    def run(
        self, table: str, table_info: DataFrame, sample_data: DataFrame
    ) -> Optional[str]:
        """
        Run the steps in a single sequence.
        """
        input_state = {
            "table": table,
            "table_info": table_info,
            "sample_data": sample_data,
        }

        steps = self._compiled_graph.stream(input_state, stream_mode="updates")

        for step in steps:
            for _, state in step.items():
                for key, value in state.items():
                    if key == "description":
                        return value
