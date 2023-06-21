# NetworkX
import networkx
from .networkx_node import NetworkXNode
from .add_node.networkx_add_node import NetworkXAddNode

#Neo4j
from neo4j import Driver as Neo4jDriver
from .neo4j_node import Neo4jNode
from .add_node.neo4j_add_node import Neo4jAddNode

def node(driver):
    if isinstance(driver, nx.Graph):
        return NetworkXNode
    elif isinstance(driver, Neo4jDriver):
        return Neo4jNode
    else:
        raise ValueError('Invalid driver type')
    
def add_node(driver, node):
    if isinstance(driver, networkx.Graph):
        return NetworkXAddNode(driver)
    elif isinstance(driver, Neo4jDriver):  
        return Neo4jAddNode(driver)
    else:
        raise ValueError('Invalid driver type')
    
