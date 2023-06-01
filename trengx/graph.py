# Ops class
import uuid
from typing import Optional, List, Dict, Union
from neo4j import GraphDatabase as graphdb

class Graph:
    """
    This class acts as an interface for executing and managing basic graph operations
    on a Neo4j graph database.

    Attributes:
        driver : A driver object that maintains the connection to the database.
    """
    def __init__(self, uri: str, user: str, password: str):
        """
        Initializes the Graph object with a connection to the database.

        Args:
            uri (str): The connection string for the database.
            user (str): The username for the database.
            password (str): The password for the database.
        """
        try:
            self.driver = graphdb.driver(uri, auth=(user, password))
        except Exception as e:
            raise Exception(f"Failed to create driver: {e}")

    def close(self) -> None:
        """
        Closes the connection to the database.
        """
        try:
            self.driver.close()
        except Exception as e:
            raise Exception(f"Failed to close driver: {e}")

    def run_query(self, query: str, parameters: Optional[Dict[str, Union[str, int]]] = None) -> List[Dict[str, Union[str, int]]]:
        """
        Runs an arbitrary Cypher query on the database.

        Args:
            query (str): The Cypher query to run.
            parameters (dict, optional): The parameters for the query. Keys are parameter names,
                and values are parameter values.

        Returns:
            list[dict]: A list of dictionaries representing the records returned by the query.
        """
        if parameters is not None and not isinstance(parameters, dict):
            raise TypeError(f"Expected dict for parameters, got {type(parameters)}")

        try:
            with self.driver.session() as session:
                result = session.run(query, parameters)
                return [record.data() for record in result]
        except Exception as e:
            raise Exception(f"Failed to run query: {e}")

    def __del__(self):
        """
        Destructor method to ensure the connection gets closed when the object is deleted.
        """
        self.close()

    # Add node   
    @staticmethod
    def _add_node_tx(tx, node_label: str, properties: dict):
        """
        Private helper function to create a node within a transaction.

        Args:
            tx: Transaction object.
            node_label (str): The label to assign to the node.
            properties (dict): Additional properties to assign to the node.

        Returns:
            dict: A dictionary representing the newly created node.
        """
        if not isinstance(node_label, str):
            raise TypeError("node_label must be a string")
        if not isinstance(properties, dict):
            raise TypeError("properties must be a dictionary")
        try:
            properties['uuid'] = str(uuid.uuid4())
            query = f"CREATE (n:{node_label} $properties) RETURN n"
            result = tx.run(query, properties=properties).single()
            node = result['n']
            node_properties = dict(node.items())
            del node_properties['uuid']
            return {'id': node['uuid'], 'label': list(node.labels), 'properties': node_properties}
        except Exception as e:
            raise Exception(f"Failed to add node: {e}")

    def add_node(self, node_label: str, properties: dict = None):
        """
        Public function to add a node in a Neo4j graph database.

        This function creates a new session and transaction with the graph database,
        and calls the helper function `_create_node_tx` to add the node.

        Args:
            node_label (str): The label to assign to the node.
            properties (dict, optional): Additional properties to assign to the node.

        Returns:
            dict: A dictionary representing the newly created node.
        """
        if properties is None:
            properties = {}

        with self.driver.session() as session:
            try:
                node = session.write_transaction(self._add_node_tx, node_label, properties)
                return node
            except Exception as e:
                raise Exception(f"Failed to add node: {e}")
            
    # Get node by id
    @staticmethod
    def _get_node_by_id_tx(tx, node_id: str):
        """
        Private helper function to retrieve a node within a transaction.

        Args:
            tx: Transaction object.
            node_id (str): The UUID of the node to retrieve.

        Returns:
            dict: A dictionary representing the retrieved node.
        """

        if not isinstance(node_id, str):
            raise TypeError("node_id must be a string")
    
        try:
            query = "MATCH (n) WHERE n.uuid = $node_id RETURN n"
            result = tx.run(query, node_id=node_id).single()
            if result is None:
                return f"No node found with node_id: {node_id}"
            else:
                node = result['n']
                if node:
                    node_properties = dict(node.items())
                    del node_properties['uuid']
                    return {'id': node['uuid'], 'label': list(node.labels), 'properties': node_properties}
        except Exception as e:
            raise Exception(f"Failed to retrieve node: {e}")

    def get_node_by_id(self, node_id: str):
        """
        Public function to retrieve a node from the graph database based on its UUID.

        This function creates a new session and transaction with the graph database,
        and calls the helper function `_get_node_by_id_tx` to retrieve the node.

        Args:
            uuid (str): The UUID of the node to retrieve.

        Returns:
            dict: A dictionary representing the retrieved node, or None if no node is found.
        """
        with self.driver.session() as session:
            try:
                return session.read_transaction(self._get_node_by_id_tx, node_id)
            except Exception as e:
                raise Exception(f"Failed to retrieve node: {e}")


    # Update node properties
    @staticmethod
    def _update_node_properties_tx(tx, node_id: str, properties: dict):
        """
        Private helper function to update node properties within a transaction.

        Args:
            tx: Transaction object.
            node_id (str): The ID of the node to update.
            properties (dict): The updated properties to assign to the node.

        Returns:
            dict: A dictionary representing the updated node, or None if no node is found.
        """
        try:
            query = "MATCH (n) WHERE id(n) = $node_id SET n += $properties RETURN n"
            result = tx.run(query, node_id=node_id, properties=properties)
            node = result.single()
            if node:
                node_properties = dict(node['n'].items())
                return {'id': node['n'].id, 'label': node['n'].labels, 'properties': node_properties}
            return None
        except Exception as e:
            raise Exception(f"Failed to update node properties: {e}")

    def update_node_properties(self, node_id: str, properties: dict):
        """
        Public function to update the properties of a node in the graph database.

        This function creates a new session and transaction with the graph database,
        and calls the helper function `_update_node_properties_tx` to update the node.

        Args:
            node_id (str): The ID of the node to update.
            properties (dict): The updated properties to assign to the node.

        Returns:
            dict: A dictionary representing the updated node, or None if no node is found.
        """
        with self.driver.session() as session:
            try:
                return session.write_transaction(self._update_node_properties_tx, node_id, properties)
            except Exception as e:
                raise Exception(f"Failed to update node properties: {e}")

    # Delete node
    @staticmethod
    def _delete_node_tx(tx, node_id: str):
        """
        Private helper function to delete a node within a transaction.

        Args:
            tx: Transaction object.
            node_id (str): The ID of the node to delete.

        Returns:
            bool: True if the node was deleted, False otherwise.
        """
        try:
            query = "MATCH (n) WHERE id(n) = $node_id DELETE n RETURN count(n) as deleted_count"
            result = tx.run(query, node_id=node_id).single()
            deleted_count = result["deleted_count"]
            if deleted_count == 0:
                return False
            return True
        except Exception as e:
            raise Exception(f"Failed to delete node: {e}")

    def delete_node(self, node_id: str):
        """
        Public function to delete a node from the graph database based on its ID.

        This function creates a new session and transaction with the graph database,
        and calls the helper function `_delete_node_tx` to delete the node.

        Args:
            node_id (str): The ID of the node to delete.

        Returns:
            bool: True if the node was deleted, False otherwise.
        """
        with self.driver.session() as session:
            try:
                return session.write_transaction(self._delete_node_tx, node_id)
            except Exception as e:
                raise Exception(f"Failed to delete node: {e}")


    #Set node value
    @staticmethod
    def _set_node_value_tx(tx, node_id:str, value):
        """
        1. MATCH path = (in1)-[r:num2op|op2num*0..]->() WHERE id(in1) = $node_id AND all(rel IN relationships(path) WHERE rel.trigger = true):
        Find a path that begins from a node (in1) which has the ID specified by the parameter node_id. 
        The path can include any number of num2op or op2num relationships (from none at all, up to an infinite number, 
        denoted by *0..). The num2op relationship likely signifies the operation to perform on a number 
        and the op2num relationship likely represents the number to perform the operation on. 
        The WHERE clause ensures all relationships in this path have a trigger property that is true.

        2. WITH path ORDER BY length(path) DESC LIMIT 1 WITH nodes(path) AS nodes:
        This statement orders all found paths by their length in descending order and limits the result to the longest path. 
        Then, the nodes of this longest path are collected into a list called nodes.

        3. UNWIND range(0, size(nodes)-2, 2) AS i WITH nodes[i] AS in1, nodes[i+1] AS op, nodes[i+2] AS out:
        The UNWIND statement creates a new row for each value in the range from 0 to the size of nodes - 2, stepping by 2. 
        This is used to group the nodes into triples (in1, op, out).

        4. MATCH (in1)-[:num2op]->(op)-[:op2num]->(out) OPTIONAL MATCH (in2)-[:num2op]->(op) WHERE id(in2) <> id(in1):
        The script then matches these triples to actual paths in the graph. It also optionally matches another node in2 that connects 
        to op with a num2op relationship, provided in2 is not the same as in1.

        5. WITH in1, op, out, in2 SET out.value = CASE ... END:
        Depending on the op.name (the name of the operation), this part updates out.value (the result of the operation). 
        For subtraction and division, it also considers a reverse property on the operation node to decide the order of the operands. 
        If op.name is none of the given, it leaves out.value as it was.
        """

        try:
            query = """
                MATCH (in1)
                WHERE id(in1) = $node_id
                SET in1.value = $value
                WITH in1
                MATCH path = (in1)-[r:num2op|op2num*0..]->()
                WHERE all(rel IN relationships(path) WHERE rel.trigger = true)
                WITH path
                ORDER BY length(path) DESC
                LIMIT 1
                WITH nodes(path) AS nodes
                UNWIND range(0, size(nodes)-2, 2) AS i
                WITH nodes[i] AS in1, nodes[i+1] AS op, nodes[i+2] AS out
                MATCH (in1)-[:num2op]->(op)-[:op2num]->(out)
                OPTIONAL MATCH (in2)-[:num2op]->(op)
                WHERE id(in2) <> id(in1)  
                WITH in1, op, out, in2
                SET out.value = 
                CASE 
                    WHEN op.name = '+' THEN in1.value + in2.value
                    WHEN op.name = '-' AND op.reverse = false THEN in1.value - in2.value
                    WHEN op.name = '-' AND op.reverse = true THEN in2.value - in1.value
                    WHEN op.name = '*' THEN in1.value * in2.value
                    WHEN op.name = '/' AND op.reverse = false THEN in1.value / in2.value
                    WHEN op.name = '/' AND op.reverse = true THEN in2.value / in1.value
                    WHEN op.name = 'round' THEN round(in1.value)
                    WHEN op.name = 'sqrt' THEN sqrt(in1.value)
                    WHEN op.name = 'abs' THEN abs(in1.value)
                    WHEN op.name = 'exp' THEN exp(in1.value)
                    WHEN op.name = 'log10' THEN log10(in1.value)
                    WHEN op.name = 'log' THEN log(in1.value)
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
            tx.run(query, node_id=node_id, value=value)
            return True
        except Exception as e:
            print(f"Error occurred: {e}")
            return False

    def set_node_value(self, node_id:str, value):
        try:
            with self.driver.session() as session:
                success = session.execute_write(self._set_node_value_tx, node_id, value)
            return success
        except Exception as e:
            print(f"Error occurred: {e}")
            return False


    @staticmethod
    def _get_node_prop_tx(tx, node_id:int, key:str):
        query = """
            MATCH (n) 
            WHERE id(n) = $node_id
            RETURN apoc.map.values(n, [$key])[0] as value
        """
        result = tx.run(query, node_id=node_id, key=key)
        record = result.single()
        return record['value']

    def get_node_prop(self, node_id:str, key:str):
        """Function for getting node property value using node ID"""
        with self.driver.session() as session:
            result = session.execute_read(self._get_node_prop_tx, node_id, key)
            return result

    
    # Remove node property
    @staticmethod
    def _remove_node_prop_tx(tx, id_key, id_value, key ):
        query = "MATCH (n) WHERE n." + id_key + " = $id_value" \
                " REMOVE n." + key
        result = tx.run(query, id_value = id_value)
        return result

    def remove_node_prop(self, id_key, id_value, key):
        """Function for removing node property value"""
        with self.driver.session() as session:
            result = session.execute_write(self._remove_node_prop_tx, id_key, id_value, key)
            return result

    # Add edge
    @staticmethod
    def _add_edge_tx(tx, edge_label:str, out_id:int, in_id:int, properties:dict, merge:bool):
        if merge:
            add_clause = "MERGE"
        else:
            add_clause = "CREATE"

        query = "MATCH (n) WHERE id(n) = $out_id" \
                " MATCH (m) WHERE id(m) = $in_id" \
                " " + add_clause + " (n)-[r:" + edge_label + "]->(m)"
        if properties:
            query += " SET r += $properties"
        query += " RETURN id(r) AS edge_id, type(r) AS edge_label, id(n) AS out_node_id, id(m) AS in_node_id, properties(r) AS properties"
        result = tx.run(query, out_id=out_id, in_id=in_id, properties=properties).data()
        return result

    def add_edge(self, edge_label:str, out_id:int, in_id:int, properties:dict=None, merge=False):
        """Function for adding edge"""
        with self.driver.session() as session:
            result = session.write_transaction(self._add_edge_tx, edge_label, out_id, in_id, properties, merge)
            return result

    # Update edge properties
    @staticmethod
    def _update_edge_properties_tx(tx, edge_label:str, out_id:int, in_id:int, properties:dict):
        query = f"""
            MATCH (n)-[r:{edge_label}]->(m)
            WHERE id(n) = $out_id AND id(m) = $in_id
            SET r += $properties
            RETURN id(r) AS edge_id, type(r) AS edge_label, id(n) AS out_node_id, id(m) AS in_node_id, properties(r) AS properties
        """
        result = tx.run(query, out_id=out_id, in_id=in_id, properties=properties).data()
        return result

    def update_edge_properties(self, edge_label:str, out_id:int, in_id:int, properties:dict):
        """Function for updating edge properties"""
        with self.driver.session() as session:
            result = session.write_transaction(self._update_edge_properties_tx, edge_label, out_id, in_id, properties)
            return result



    # Delete edge
    @staticmethod
    def _delete_edge_tx(tx, edge_label:str, out_id:int, in_id:int):
        query = "MATCH (n)-[r:" + edge_label + "]->(m)" \
                " WHERE id(n) = $out_id AND id(m) = $in_id" \
                " DELETE r" \
                " RETURN id(r) as deleted_edge_id"
        result = tx.run(query, out_id=out_id, in_id=in_id).data()
        return result

    def delete_edge(self, edge_label:str, out_id:int, in_id:int):
        """Function for deleting edge"""
        with self.driver.session() as session:
            result = session.execute_write(self._delete_edge_tx, edge_label, out_id, in_id)
            return result

    # Delete all
    @staticmethod
    def _delete_all_tx(tx):
        query = "MATCH (n)\n" \
                "OPTIONAL MATCH (n)-[r]-()\n" \
                "DELETE n, r"
        tx.run(query)
    
    def delete_all(self):
        """Function for deleting all nodes and relationships"""
        with self.driver.session() as session:
            session.write_transaction(self._delete_all_tx)
        return {'status': 'deleted all'}
