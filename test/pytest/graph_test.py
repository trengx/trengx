import os
import sys
import pytest
from neo4j import GraphDatabase as graphdb

sys.path.append('trengx')
import graph

# .env secrets
uri = os.environ['NEO4J_URI'] # Get the value of the uri variable
user = os.environ['NEO4J_USER'] # Get the value of the user variable
password= os.environ['NEO4J_PASSWORD']  # Get the value of the pw variable

# Create a Graph class instance
g = graph.Graph(graphdb, uri, user, password)

def test_add_node_with_all_required_properties():
    # Add a node with all required properties
    node = g.add_node('num', {'name': 'Node 1', 'value': 2.0})
    assert node is not None
    assert 'id' in node
    assert 'label' in node
    assert 'properties' in node
    assert node['properties']['name'] == 'Node 1'
    assert node['properties']['value'] == 2.0


def test_add_node_without_properties():
    # Add a node without properties
    node = g.add_node('num', 'Node 2')
    assert node is not None
    assert 'id' in node
    assert 'label' in node
    assert 'name' in node
    assert 'properties' in node

def test_add_node_with_additional_properties():
    # Add a node with additional properties
    node = g.add_node('num', 'Node 3', {'value': 4.0, 'description': 'This is Node 3'})
    assert node is not None
    assert 'id' in node
    assert 'label' in node
    assert 'name' in node
    assert 'properties' in node
    assert node['name'] == 'Node 3'
    assert node['properties']['value'] == 4.0
    assert node['properties']['description'] == 'This is Node 3'

def test_delete_node():
    """Function for testing delete_node"""
    node = g.add_node ('num', 'node', {'value': 2.0})
    node_id = node['node_id']
    assert g.delete_node(node_id) == {'deleted_node_id': node_id}

def test_do_math():
    """Function for testing do_math"""

    in_1 = g.add_node ('num', 'in_1', {'value': 2.0})
    in_1_id = in_1['node_id']
    print (in_1_id)
    in_2 = g.add_node ('num', 'in_2', {'value': 3.0})
    in_2_id = in_2['node_id']
    print (in_2_id)
    add = g.add_node ('op', '+', {'reverse': False})
    add_id = add['node_id']
    print (add_id)
    g.add_edge ('num2op', in_1_id, add_id)
    g.add_edge ('num2op', in_2_id, add_id)
    out = g.add_node ('num', 'out', {'value': 0.0})
    out_id = out['node_id']
    print (out_id)
    g.add_edge ('op2num', add_id, out_id)
    assert g.do_math(in_1_id) == (out_id, 'out', 5.0)

def test_delete_all():
    """Function for testing delete_all"""
    assert g.delete_all() == {'status': 'deleted all'}

g.close()
