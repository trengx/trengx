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
            query = "MERGE (n:" + node_label + "{ name: $name })" \
                    " SET n += $properties" \
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

    @staticmethod
    def _delete_node_tx(tx, node_id:int):
        query = "MATCH (n) WHERE id(n) = $node_id" \
                " DELETE n" \
                " RETURN id(n) AS deleted_node_id"
        result = tx.run(query, node_id=node_id).single()
        return {'deleted_node_id': result["deleted_node_id"]}

    def delete_node(self, node_id:int):
        """Function for deleting node using node id"""
        with self.driver.session() as session:
            deleted_node_id = session.write_transaction(self._delete_node_tx, node_id)
            return {'deleted_node_id': deleted_node_id['deleted_node_id']}
    
    # perform math operation
    @staticmethod
    def _do_math_tx(tx, node_id:int):
        query = "MATCH (in1)-[:num2op]->(o:op)" \
            " OPTIONAL MATCH (in1)-[:num2op]->(o)<-[:num2op]-(in2)" \
            " MATCH (o)-[:op2num]->(out)" \
            " WHERE id(in1) = $node_id" \
            " WITH id(out) AS out_id, out.name AS out_name, out, CASE o.name" \
            "    WHEN '+' THEN in1.value + in2.value" \
            "    WHEN '-' THEN in1.value - in2.value" \
            "    WHEN '*' THEN in1.value * in2.value" \
            "    WHEN '/' THEN in1.value / in2.value" \
            "    WHEN '%' THEN in1.value % in2.value" \
            "    WHEN '^' THEN in1.value ^ in2.value" \
            "    WHEN 'sqrt' THEN sqrt(in1.value)" \
            "    WHEN 'abs' THEN abs(in1.value)" \
            "    WHEN 'exp' THEN exp(in1.value)" \
            "    WHEN 'log10' THEN log10(in1.value)" \
            "    WHEN 'log' THEN log(in1.value)" \
            "    WHEN 'sin' THEN sin(in1.value)" \
            "    WHEN 'cos' THEN cos(in1.value)" \
            "    WHEN 'tan' THEN tan(in1.value)" \
            "    WHEN 'ceil' THEN ceil(in1.value)" \
            "    WHEN 'floor' THEN floor(in1.value)" \
            "    WHEN 'round' THEN round(in1.value)" \
            "    WHEN 'sign' THEN sign(in1.value)" \
            "    ELSE out.value" \
            " END AS value" \
            " SET out.value = value" \
            " RETURN out_id, out_name, out.value AS out_value"
        result = tx.run(query, node_id=node_id).data()
        for record in result:
            out_id = record['out_id']
            out_name = record['out_name']
            out_value = record['out_value']
            print(f'out_id: {out_id}')
            print(f'out_name: {out_name}')
            print(f'out_value: {out_value}')
        return out_id, out_name, out_value
    
    def do_math(self, node_id:int):
        """Function for doing math"""
        with self.driver.session() as session:
            result = session.execute_write(self._do_math_tx, node_id)
            self.set_node_prop(result[0], result[1], result[2], True)
            return result

    # check the presence of outgoing edge
    @staticmethod
    def _check_outgoing_edge_tx(tx, node_id):
        query = "MATCH (n)-[label:num2op]->()" \
                " WHERE id(n) = $node_id" \
                " RETURN COUNT(label) > 0 as has_outgoing_label"
        result = tx.run(query, node_id=node_id)
        has_outgoing_edge = result.single()[0]
        return has_outgoing_edge

    def check_outgoing_edge(self, node_id:int):
        """Function for checking the presence of outgoing edge"""
        with self.driver.session() as session:
            result = session.execute_write(self._check_outgoing_edge_tx, node_id)
            return result 
    
    # set node property value
    @staticmethod
    def _set_node_prop_tx(tx, node_id:int, key:str, value):
        query = "MATCH (n) WHERE id(n) = $node_id" \
                " SET n." + key + " = $value" \
                " RETURN n" 
        result = tx.run(query, node_id=node_id, value=value)
        record = result.single()
        node = record['n']
        node_properties = dict(node.items())
        return {'node_id': node.id, 'properties': node_properties}
    
    def set_node_prop(self, node_id:int, key:str, value, do_math):
        """Function for setting node property value"""
        results = []
        with self.driver.session() as session:
            result1 = session.execute_write(self._set_node_prop_tx, node_id, key, value)
            results.append(result1)
            if do_math is True:
                outgoing_edge = self.check_outgoing_edge(node_id)
                if outgoing_edge is True:
                    result2 = self.do_math(node_id)
                    results.append(result2)
        return results

    # Get node property value
    @staticmethod
    def _get_node_prop_tx(tx, id_key, id_value, key ):
        query = "MATCH (n) WHERE n." + id_key + " = $id_value" \
                " RETURN n." + key + " as value"
        result = tx.run(query, id_value = id_value)
        return result.single()[0]

    def get_node_prop(self, id_key, id_value, key):
        """Function for getting node property value"""
        with self.driver.session() as session:
            result = session.execute_write(self._get_node_prop_tx, id_key, id_value, key)
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
