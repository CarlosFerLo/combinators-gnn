import pytest
import implica as imp
from combinators_gnn.graph_engine.engine import GraphEngine


@pytest.fixture(scope="module")
def var_A():
    return imp.var("A")


@pytest.fixture(scope="module")
def var_B():
    return imp.var("B")


@pytest.fixture(scope="module")
def var_C():
    return imp.var("C")


@pytest.fixture
def engine_factory():
    """Factory fixture to create GraphEngine instances for provided start/end types.

    Usage:
        engine = engine_factory(start_type, end_type)
    """

    def _factory(start, end):
        return GraphEngine(start, end)

    return _factory
