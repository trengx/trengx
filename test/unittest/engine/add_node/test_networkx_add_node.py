import unittest
import networkx as nx
import sys
sys.path.append('trengx/engine/add_node')
from networkx_add_node import Node


class NetworkXAddNodeTestCase(unittest.TestCase):
    def setUp(self):
        self.graph = nx.Graph()

    def test_add_to_graph(self):
        node = Node(self.graph, name="Node 1", value=42, grad=0.5)
        self.assertTrue(self.graph.has_node(node.id))
        created_node = self.graph.nodes[node.id]
        self.assertEqual(created_node["name"], "Node 1")
        self.assertEqual(created_node["value"], 42)
        self.assertEqual(created_node["grad"], 0.5)


if __name__ == "__main__":
    unittest.main()
