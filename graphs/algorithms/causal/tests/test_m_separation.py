import networkx as nx
import pytest

from graphs import MixedEdgeGraph
from graphs.algorithms.causal import m_separated


def test_m_separation():
    digraph = nx.path_graph(4)
    digraph.add_edge(2, 4)
    bigraph = nx.Graph([(2, 3)])
    bigraph.add_nodes_from(digraph)
    G = MixedEdgeGraph([digraph, bigraph], ["directed", "bidirected"])

    # error should be raised if someone does not use a MixedEdgeGraph
    with pytest.raises(RuntimeError, match="m-separation should only be run on a MixedEdgeGraph"):
        m_separated(digraph, {0}, {1}, set())

    print(G.edges())
    # basic d-separation statements based on blocking paths should work
    assert not m_separated(G, {0}, {3}, set())
    assert m_separated(G, {0}, {3}, {1})

    # conditioning on a collider via bidirected edge opens the collider
    assert not m_separated(G, {0}, {3}, {2})
    assert m_separated(G, {0}, {3}, {1, 2})

    # conditioning on a descendant of a collider via bidirected edge opens the collider
    assert not m_separated(G, {0}, {3}, {4})
