import unittest
import networkx as nx
import sys
sys.path.append('trengx/engine')
from operation_2 import Operation_2

class TestOperation2(unittest.TestCase):
    def setUp(self):
        self.graph = nx.DiGraph()
        self.operation_2 = Operation_2(self.graph, input1_name='input1', input1_value=5, operation_name='add', 
                                       input2_name='input2', input2_value=6, output_name='output', output_value=11)
        self.input1_id, self.input2_id, self.operation_id, self.output_id = self.operation_2.create_graph()

    def test_nodes(self):
        self.assertIn(self.input1_id, self.graph.nodes)
        self.assertIn(self.input2_id, self.graph.nodes)
        self.assertIn(self.operation_id, self.graph.nodes)
        self.assertIn(self.output_id, self.graph.nodes)

    def test_edges(self):
        self.assertIn((self.input1_id, self.operation_id), self.graph.edges)
        self.assertIn((self.input2_id, self.operation_id), self.graph.edges)
        self.assertIn((self.operation_id, self.output_id), self.graph.edges)

    def test_node_values(self):
        self.assertEqual(self.graph.nodes[self.input1_id]['value'], 5)
        self.assertEqual(self.graph.nodes[self.input2_id]['value'], 6)
        self.assertEqual(self.graph.nodes[self.output_id]['value'], 11)

    def test_operation_name(self):
        self.assertEqual(self.graph.nodes[self.operation_id]['name'], 'add')

if __name__ == '__main__':
    unittest.main()
