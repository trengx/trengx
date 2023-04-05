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
g.delete_all()
print (g.add_node ('num', 34, {'value': 2.0}))
