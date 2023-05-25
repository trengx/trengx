# Graph class
"""Module providing basic graph queries (Neo4j Cypher)"""
class Graph:
    """Class for providing basic graph queries (Neo4j Cypher)"""
    # Initialize graph database class
    def __init__(self, graphdb, uri, user, password):
        self.driver = graphdb.driver(uri, auth=(user, password))

    # Close session
    def close(self)-> None:
        """Function for session closing"""
        self.driver.close()

    # Add node
    @staticmethod
    def _add_node_tx(tx, node_label:str, name:str, properties:dict, merge:bool):
        if merge:
            if not properties:
                query = "MERGE (n:" + node_label + "{ name: $name })" \
                        " RETURN n"
            else:
                query = "MERGE (n:" + node_label + "{ name: $name })" \
                        " SET n += $properties" \
                        " RETURN n"
        else:
            if not properties:
                query = "CREATE (n:" + node_label + "{ name: $name })" \
                        " RETURN n"
            else:
                query = "CREATE (n:" + node_label + "{ name: $name })" \
                        " SET n += $properties" \
                        " RETURN n"
        result = tx.run(query, name=name, properties=properties).single()
        node = result['n']
        node_properties = dict(node.items())
        return {'node_id': node.id, 'node_label': node.labels, 'properties': node_properties}

    def add_node(self, node_label:str, name:str, properties:dict, merge=False):
        """Function for creating or merging node
        Node name (property) should be given)"""
        with self.driver.session() as session:
            node = session.write_transaction(self._add_node_tx, node_label, name, properties, merge)
            return node

    # Delete node
    @staticmethod
    def _delete_node_tx(tx, node_id:int):
        query = "MATCH (n) WHERE id(n) = $node_id" \
                " DELETE n" \
                " RETURN id(n) AS deleted_node_id"
        result = tx.run(query, node_id=node_id).single()
        if result is None:
            return None
        return {'deleted_node_id': result['deleted_node_id']}

    def delete_node(self, node_id:int):
        """Function for deleting node using node id"""
        with self.driver.session() as session:
            result = session.write_transaction(self._delete_node_tx, node_id)
            if result is None:
                return None
            return result

    @staticmethod
    def _set_node_prop_tx(tx, node_id:int, key:str, value):
        query = """
            MATCH (n)
            WHERE id(n) = $node_id
            OPTIONAL MATCH (n)-[r:num2op {trigger:true}]->(o:op)<-[:num2op]-(in2)
            OPTIONAL MATCH (o)-[:op2num]->(out)
            WITH 
                n, 
                o, 
                in2, 
                out,
                CASE 
                    WHEN r IS NULL THEN false 
                    ELSE true 
                END as has_outgoing_edge,
                CASE o.name
                    WHEN '+' THEN n.value + in2.value
                    WHEN '-' THEN 
                        CASE WHEN o.reverse THEN in2.value - n.value ELSE n.value - in2.value END
                    WHEN '*' THEN n.value * in2.value
                    WHEN '/' THEN
                        CASE WHEN o.reverse THEN in2.value / n.value ELSE n.value / in2.value END
                END AS math_result
            CALL apoc.create.setProperty(n, $key, CASE
                WHEN has_outgoing_edge THEN math_result
                ELSE $value
                END) YIELD node
            RETURN id(node) as node_id, node
        """
        result = tx.run(query, node_id=node_id, key=key, value=value)
        record = result.single()
        node = record['node']
        node_properties = dict(node.items())
        return {'node_id': record['node_id'], 'properties': node_properties}

    def set_node_prop(self, node_id:int, key:str, value):
        with self.driver.session() as session:
            result = session.execute_write(self._set_node_prop_tx, node_id, key, value)
            return result

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

    def get_node_prop(self, node_id:int, key:str):
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
