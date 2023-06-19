from neo4j import Driver as Neo4jDriver
import networkx 
from .networkx_add_edge import NetworkXAddEdge
from .neo4j_add_edge import Neo4jAddEdge

def edge(driver, node1, node2, id=None, label=None, second_operand=None):
    if isinstance(driver, networkx.Graph):
        return NetworkXAddEdge(driver, node1, node2, id, label, second_operand)
    elif isinstance(driver, Neo4jDriver):
        return Neo4jAddEdge(driver, node1, node2, id, label, second_operand)
    else:
        raise ValueError('Invalid driver type')
