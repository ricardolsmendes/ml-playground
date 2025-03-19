from typing import List, Mapping, Optional

from langgraph import graph
from langgraph.checkpoint import memory
from pandas import DataFrame

import components
from components import State


class MetadataEnrichmentAssistant:

    def __init__(self):
        self._metadata_enrichment_agent = components.MetadataBooster()

        checkpointer = memory.MemorySaver()
        graph_builder = graph.StateGraph(State).add_sequence(
            [self._generate_table_description, self._accept_content]
        )
        graph_builder.add_edge(graph.START, "_generate_table_description")
        self._graph = graph_builder.compile(
            checkpointer=checkpointer, interrupt_before=["_accept_content"]
        )

    def _generate_table_description(self, state: State) -> Mapping[str, str]:
        return self._metadata_enrichment_agent.generate_table_description(state)

    @classmethod
    def _accept_content(cls, state: State) -> Mapping[str, bool]:
        return components.ContentAcceptanceHelper.accept()

    @classmethod
    def _convert_df_to_text(cls, df: DataFrame) -> List[str]:
        return [
            ", ".join([f"{col}: {row[col]}" for col in df.columns])
            for _, row in df.iterrows()
        ]

    def run(
        self, table: str, columns_technical_metadata: DataFrame, sample_data: DataFrame
    ) -> Optional[str]:
        """
        Run the steps in a single sequence.
        """
        initial_state = {
            "table": table,
            "columns_technical_metadata": self._convert_df_to_text(
                columns_technical_metadata
            ),
            "sample_data": self._convert_df_to_text(sample_data),
            "accepted": False,
        }

        # Now that we're using persistence, we need to specify a thread ID
        # so that we can continue the run after review.
        config = {"configurable": {"thread_id": "1"}}

        description = None
        steps = self._graph.stream(initial_state, config, stream_mode="updates")
        for step in steps:
            for _, result in step.items():
                if "description" in result:
                    description = result.get("description")
                    print(f"\n\n\nTable: {table}\n" f"Description: {description}\n\n")

        user_approval = input("Use the above description? (y/n/r): ")
        if user_approval.lower() == "n":
            print("Content rejected by user.")
            return None
        if user_approval.lower() == "r":
            print("Retrying...")
            return self.run(table, columns_technical_metadata, sample_data)

        # If approved, continue the graph execution
        steps = self._graph.stream(None, config, stream_mode="updates")
        for step in steps:
            for _, result in step.items():
                if "accepted" in result and result.get("accepted"):
                    return description

        return None
