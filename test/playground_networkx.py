import networkx as nx
import uuid
import sys
sys.path.append('../trengx')
import trengx as t

# Create a directed graph
g = nx.DiGraph()

# Create nodes
id1 = str(uuid.uuid1())
node1 = t.node(id=id1, label='num', name="x", value=2, grad=0.1)
t.add_node(g, node1)
id2 = str(uuid.uuid1())
node2 = t.node(id=id2, label='op', name="sin")
t.add_node(g, node2)
print (node1.id)

# Create edge
id3 = str(uuid.uuid1())
edge = t.edge(g, id=id3, label='num2op', source=node1.id, target=node2.id, second_operand=False)
t.add_edge(g, edge)

print(node1)
print(node2)
print(edge)