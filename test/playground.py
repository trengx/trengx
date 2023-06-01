import os
import sys
import pytest
from neo4j import GraphDatabase as graphdb

sys.path.append('trengx')
import graph

# Retrieve secrets (confidential credentials) from environment variables stored in .env file
uri = os.getenv('NEO4J_URI') # Get the value of the uri variable
user = os.getenv('NEO4J_USER') # Get the value of the user variable
password= os.getenv('NEO4J_PASSWORD')  # Get the value of the pw variable

# Create a Graph class instance
g = graph.Graph(graphdb, uri, user, password)

# Create a Graph class instance
g = graph.Graph(graphdb, uri, user, password)


g.add('num', 'Node 1', {'value': 2.0})