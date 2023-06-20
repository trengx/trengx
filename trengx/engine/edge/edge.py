import uuid

class Edge:
    def __init__(self, id=None, label=None, source=None, target=None, name=None, second_operand=None):
        self.id = id or str(uuid.uuid1())
        self.label = label
        self.source = source
        self.target = target
        self.name = name
        self.second_operand = second_operand
        
    def __str__(self):
        return str({
            'id': self.id,
            'label': self.label,
            'source': self.source,
            'target': self.target,
            'name': self.name,
            'second_operand': self.second_operand
        })