import os 
from neo4j import GraphDatabase as graphdb
import sys
sys.path.append('trengx')
import graph

# Codespaces secrets
uri = os.environ['NEO4J_URI'] # Get the value of the uri variable
user = os.environ.get("NEO4J_USER") # Get the value of the user variable
password= os.getenv("NEO4J_PASSWORD")  # Get the value of the pw variable

# Create Graph Class
g = graph.Graph(graphdb, uri, user, password)


def test_add_node():
    node = g.add_node ('num', 'y_i', {'value': 2.0})
    assert node['properties'] == {'name': 'y_i', 'value': 2.0}

def test_delete_node():
    node = g.add_node ('num', 'node', {'value': 2.0})
    node_id = node['node_id']
    assert g.delete_node(node_id) == {'deleted_node_id': node_id}



    
print (node_id)
print (g.delete_node(node_id))      

g.close()