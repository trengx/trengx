import unittest
import networkx as nx
import sys
sys.path.append('trengx/engine')
from add_edge import AddEdge

class AddEdgeTestCase(unittest.TestCase):
    def setUp(self):
        self.graph = nx.Graph()
        self.source_node = "Node 1"
        self.target_node = "Node 2"
        self.weight = 0.5
        self.edge = AddEdge(self.graph, self.source_node, self.target_node, self.weight)

    def test_add_to_graph(self):
        self.edge.add_to_graph()
        created_edge = self.graph.edges[self.source_node, self.target_node]
        self.assertIn((self.source_node, self.target_node), self.graph.edges)
        self.assertEqual(created_edge["weight"], self.weight)

if __name__ == "__main__":
    unittest.main()
