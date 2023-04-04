# pip install neo4j==5.7.0

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


# e[i] = y[i] - y_est[i]
y_i = g.add_node ('num', 'y_i', {'value': 2.0})
y_i_id = y_i['node_id']
y_est_i = g.add_node ('num', 'y_est_i', {'value': 3.0})
y_est_i_id = y_est_i['node_id']
sub = g.add_node ('op', '%', {'reverse':False})
sub_id = sub['node_id']
g.add_edge ('num2op', y_i_id, sub_id)
g.add_edge ('num2op', y_est_i_id, sub_id)
e_i = g.add_node ('num', 'e_i', {'value': 0.0})
e_i_id = e_i['node_id']
g.add_edge ('op2num', sub_id, e_i_id)

g.set_node_prop(y_i_id, 'value', 4, True)