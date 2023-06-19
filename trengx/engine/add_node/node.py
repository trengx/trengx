from neo4j import Driver as Neo4jDriver
import networkx 
from .networkx_add_node import NetworkXAddNode
from .neo4j_add_node import Neo4jAddNode

def node(driver, id=None, label=None, name=None, value=None, grad=None):
    if isinstance(driver, networkx.Graph):
        return NetworkXAddNode(driver, id, label, name, value, grad)
    elif isinstance(driver, Neo4jDriver):
        return Neo4jAddNode(driver, id, label, name, value, grad)
    else:
        raise ValueError('Invalid driver type')