import os
from dotenv import load_dotenv
from neo4j import GraphDatabase as graphdb
import sys
sys.path.append('trengx')
import graph


load_dotenv()  # Load environment variables from .env file
uri = os.getenv("uri")  # Get the value of the uri variable
user = os.getenv("user")  # Get the value of the user variable
password = os.getenv("password")  # Get the value of the pw variable
g = graph.Graph(graphdb, uri, user, password)


x = g.add_node ('num', 'x', merge=True)
x_id = x['node_id']
g.set_node_prop(x_id, 'value', 2.0, False)

y = g.add_node ('num', 'y', merge=True)
y_id = y['node_id']
g.set_node_prop(y_id, 'value', 3.0, False)

op = g.add_node ('op', '*',  merge=True)
op_id = op['node_id']

g.add_edge('num2op', x_id, op_id, merge=True)
g.add_edge('num2op', y_id, op_id, merge=True)

z = g.add_node ('num', 'z', merge=True)
z_id = z['node_id']
g.set_node_prop(z_id, 'value', 0.0, False)
g.add_edge('op2num',op_id, z_id, merge=True)

t = g.add_node ('num', 't', merge=True)
t_id = t['node_id']
g.set_node_prop(t_id, 'value', 2.0, False)

op2 = g.add_node ('op', '+',  merge=True)
op2_id = op2['node_id']

g.add_edge('num2op', z_id, op2_id, merge=True)
g.add_edge('num2op', t_id, op2_id, merge=True)

s = g.add_node ('num', 's', merge=True)
s_id = s['node_id']
g.set_node_prop(s_id, 'value', 0.0, False)
g.add_edge('op2num',op2_id, s_id, merge=True)

g.set_node_prop(x_id, 'value', 2.0, do_math=True)