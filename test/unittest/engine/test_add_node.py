import unittest
import uuid
import networkx as nx
import sys
sys.path.append('trengx/engine')
from add_node import AddNode 

class AddNodeTestCase(unittest.TestCase):
    def setUp(self):
        self.graph = nx.Graph()
        self.node_name = "Node 1"
        self.node_value = 42
        self.node_grad = 0.5

    def test_create_node_with_defaults(self):
        node = AddNode(self.graph)
        self.assertIsInstance(node, AddNode)
        self.assertIsNotNone(uuid.UUID(node.id, version=1))
        self.assertIsNone(node.name)
        self.assertIsNone(node.value)
        self.assertIsNone(node.grad)

    def test_create_node_with_values(self):
        node_id = "custom_id"
        node = AddNode(self.graph, id=node_id, name=self.node_name, value=self.node_value, grad=self.node_grad)
        self.assertIsInstance(node, AddNode)
        self.assertEqual(node.id, node_id)
        self.assertEqual(node.name, self.node_name)
        self.assertEqual(node.value, self.node_value)
        self.assertEqual(node.grad, self.node_grad)

    def test_add_to_graph(self):
        node = AddNode(self.graph, name=self.node_name, value=self.node_value, grad=self.node_grad)
        node_id, created_node = node.add_to_graph()
        self.assertIn(node_id, self.graph.nodes)
        self.assertEqual(self.graph.nodes[node_id]["name"], self.node_name)
        self.assertEqual(self.graph.nodes[node_id]["value"], self.node_value)
        self.assertEqual(self.graph.nodes[node_id]["grad"], self.node_grad)
        self.assertEqual(created_node, self.graph.nodes[node_id])
        print (self.graph.nodes[node_id])

if __name__ == '__main__':
    unittest.main()
