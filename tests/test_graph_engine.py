import implica as imp


class TestGraphEngine:
    def test_engine_adds_start_and_end_nodes(self, var_A, var_B, engine_factory):
        A = var_A
        B = var_B

        # Start: A -> B, End: B
        start = imp.app(A, B)
        end = B

        engine = engine_factory(start, end)

        start_node = engine.get_start_node()
        end_node = engine.get_end_node()

        assert start_node.type.uid == start.uid
        assert end_node.type.uid == end.uid

        # Graph should have at least the two nodes
        assert engine.graph.has_node(start_node.uid)
        assert engine.graph.has_node(end_node.uid)

    def test_engine_collects_variable_nodes_and_duplicates(
        self, var_A, var_B, engine_factory
    ):
        A = var_A
        B = var_B

        # Start uses A twice, end uses A and B
        start = imp.app(A, imp.app(A, B))  # A -> (A -> B)
        end = imp.app(A, B)

        engine = engine_factory(start, end)

        var_nodes = engine.get_variable_nodes()

        # get_variable_nodes returns Node objects created from var_types (which is a concat)
        var_uids = [n.type.uid for n in var_nodes]

        # var_types in engine is start.variables + end.variables
        expected_vars = start.variables + end.variables
        expected_uids = [v.uid for v in expected_vars]

        assert var_uids == expected_uids

        # Graph should contain nodes for each unique variable uid
        unique_expected = set(expected_uids)
        for uid in unique_expected:
            assert engine.graph.has_node(uid)

    def test_graph_nodes_count_matches_expected(
        self, var_A, var_B, var_C, engine_factory
    ):
        A = var_A
        B = var_B
        C = var_C

        start = imp.app(A, imp.app(B, C))
        end = imp.app(B, C)

        engine = engine_factory(start, end)

        # Nodes added: start type, end type, and all variable types (A,B,C)
        # Note: variable types might include duplicates; count unique nodes in the graph
        nodes = list(engine.graph.nodes())
        uids = {n.uid for n in nodes}

        # Should contain start and end uids
        assert start.uid in uids
        assert end.uid in uids

        # Variables A,B,C should be present
        assert A.uid in uids
        assert B.uid in uids
        assert C.uid in uids

        # At minimum 5 nodes (start, end, A, B, C) but depending on structure
        assert engine.graph.node_count() >= 5
