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
g = graph.Graph(uri, user, password)

query="""
    MATCH (in1)
    WHERE in1.uuid = $node_id
    SET in1.value = $value
    WITH in1
    MATCH path = (in1)-[r:num2op|op2num*0..]->()
    WHERE all(rel IN relationships(path) WHERE rel.trigger = true)
    WITH path
    ORDER BY length(path) DESC
    LIMIT 1
    WITH nodes(path) AS nodes
    UNWIND range(0, size(nodes)-2, 2) AS i
    WITH nodes[i] AS in1, nodes[i+1] AS op, nodes[i+2] AS out, nodes
    MATCH (in1)-[:num2op]->(op)-[:op2num]->(out)
    OPTIONAL MATCH (in2)-[:num2op]->(op)
    WHERE in1.uuid  <> in2.uuid
    WITH in1, op, out, in2
    SET out.value = 
    CASE 
        WHEN op.name = '+' THEN in1.value + in2.value
        WHEN op.name = '-' AND op.reverse = false THEN in1.value - in2.value
        WHEN op.name = '-' AND op.reverse = true THEN in2.value - in1.value
        WHEN op.name = '*' THEN in1.value * in2.value
        WHEN op.name = '/' AND op.reverse = false AND in2.value <> 0 THEN in1.value / in2.value
        WHEN op.name = '/' AND op.reverse = true AND in1.value <> 0 THEN in2.value / in1.value
        WHEN op.name = 'sqrt' AND in1.value >= 0 THEN sqrt(in1.value)
        WHEN op.name = 'abs' THEN abs(in1.value)
        WHEN op.name = 'exp' THEN exp(in1.value)
        WHEN op.name = 'log10' AND in1.value > 0 THEN log10(in1.value)
        WHEN op.name = 'log' AND in1.value > 0 THEN log(in1.value)
        WHEN op.name = 'sin' THEN sin(in1.value)
        WHEN op.name = 'cos' THEN cos(in1.value)
        WHEN op.name = 'tan' THEN tan(in1.value)
        WHEN op.name = 'ceil' THEN ceil(in1.value)
        WHEN op.name = 'floor' THEN floor(in1.value)
        WHEN op.name = 'round' THEN round(in1.value)
        WHEN op.name = 'sign' THEN sign(in1.value)
        WHEN op.name = 'store' THEN in1.value
        ELSE out.value
    END
"""

# Define the parameters for Sthe query.
parameters = {'node_id': 'e0aab6b8-e5f5-4b66-9bbc-4a8fa6da6b8f', 'value': 10}

# Use the run_query method to execute the query and fetch the results.
results = g.run_query(query, parameters)
g.close()

# Print the results.
print (results)