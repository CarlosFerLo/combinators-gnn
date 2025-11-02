from __future__ import annotations

from typing import Set, List

import implica as imp
from .strategy import GenerationStrategy


class GraphEngine:
    """Build a small implicational-logic graph for a generation goal.

    The engine expects two types: `start` and `end`. It will create a
    `Graph`, add nodes corresponding to the `start` and `end` types and also
    add nodes for every base `Variable` that appears inside those types.

    Attributes:
        start_type: The goal start type
        end_type: The goal end type
        graph: The underlying implica Graph instance
        start_node_uid: UID of the start node
        end_node_uid: UID of the end node
        variable_nodes: Mapping from variable uid to Node for all discovered variables
    """

    def __init__(
        self,
        start: imp.BaseType,
        end: imp.BaseType,
        generation_strategy: GenerationStrategy,
    ):
        self.start_type = start
        self.end_type = end

        # Save the generation strategy (may be extended later)
        self.generation_strategy = generation_strategy

        # Create a fresh graph
        self.graph = imp.Graph()
        # Create a connection and add the start/end nodes plus variable nodes
        conn = self.graph.connect()

        # Add start and end nodes

        start_node = imp.node(self.start_type)
        end_node = imp.node(self.end_type)

        with self.graph.connect() as conn:
            conn.add_node(start_node)
            conn.add_node(end_node)

        # Collect all variable types from start and end
        var_types = start.variables + end.variables

        # Add nodes for each variable type
        with self.graph.connect() as conn:
            conn.try_add_many_nodes([imp.node(t) for t in var_types])

        # Save uids/mappings
        self.start_node_uid = start_node.uid
        self.end_node_uid = end_node.uid
        self.var_types = var_types

    def get_start_node(self):
        return self.graph.get_node(self.start_node_uid)

    def get_end_node(self):
        return self.graph.get_node(self.end_node_uid)

    def get_variable_nodes(self) -> List[imp.Node]:
        """Return list of Node for all base variable nodes discovered."""
        return [imp.node(t) for t in self.var_types]
