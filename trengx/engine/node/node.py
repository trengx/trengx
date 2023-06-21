import uuid

class Node:
    def __init__(self, id=None, label=None, name=None, value=None, grad=None):
        self.id = id or str(uuid.uuid1())
        self.label = label
        self.name = name
        self.value = value
        self.grad = grad

    def __str__(self):
        return str({
            'id': self.id,
            'label': self.label,
            'name': self.name,
            'value': self.value,
            'grad': self.grad
        })