from .add_edge import AddEdge

class Neo4jAddEdge(AddEdge):
    
    def __init__(self, driver, edge):
        super().__init__(driver, edge)
        self.edge_created = False
        self.edge_properties = {}
        self.execute()
        
    def execute(self):
        with self.driver.session() as session:
            response = session.run(
                f"""
                MATCH (a),(b) 
                WHERE a.id = $source AND b.id = $target
                CREATE (a)-[r:{self.label} {{id: $id, name: $name, second_operand: $second_operand}}]->(b)
                RETURN r
                """,
                source=self.source, 
                target=self.target,
                id=self.id, 
                name=self.name, 
                second_operand=self.second_operand
            ).single()
       
        if response:
            self.edge_created = True
            edge = response['r']
            self.edge_properties = dict(edge.items())
        
    def get_edge_properties(self):
        return self.edge_properties
    
    def __str__(self):
        if self.edge_created:
            return str(self.get_edge_properties())
        else:
            return "Edge not created."
