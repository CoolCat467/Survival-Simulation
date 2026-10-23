class inputNode:
    def __init__(self,n):
        self.outputs = []#list of nodes
        self.weights = []#list of weights
        self.value = 0
        self.name = n

    def setValue(self, v):
        self.value = v
    
    def getValue(self):
        return self.value

class outputNode:
    def __init__(self,n):
        self.inputs = []
        self.weights = []
        self.value = 0
        self.name = n

    def getValue(self):
        return self.value
