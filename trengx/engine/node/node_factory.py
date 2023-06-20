# NetworkX
import networkx
from .add_node.networkx_add_node import NetworkXAddNode

#Neo4j
from neo4j import Driver as Neo4jDriver
from .add_node.neo4j_add_node import Neo4jAddNode

def add_node(driver, node):
    if isinstance(driver, networkx.Graph):
        return NetworkXAddNode(driver, node)
    elif isinstance(driver, Neo4jDriver):  
        return Neo4jAddNode(driver, node)
    else:
        raise ValueError('Invalid driver type')
    
