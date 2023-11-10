from enum import Enum
import itertools

class Gate(Enum):
    AND = "and"
    OR = "or"
    
class BoolFunction:
    def __init__(self, value=None, children=[], gate=None):
        self.value = value
        self.children = children
        self.gate = gate
        self.gateOperator = None
        if (self.gate == Gate.AND):
            self.gateOperator = all
        elif (self.gate == Gate.OR):
            self.gateOperator = any

    def getVars(self):
        vars = []
        for child in self.children:
            if (child.children != []):
                vars.extend(child.getVars())
            else:
                vars.append(child)
        return vars
    
    def evaluate(self):
        childrenValues = []
        for child in self.children:
            if (self.gate != None):
                childrenValues.append(child.evaluate())
            else:
                return self.value
        if (self.gate == None):
            return self.value
        return self.gateOperator(childrenValues)

def exampleFunction():
    v1 = BoolFunction(1)
    v2 = BoolFunction(1)
    v3 = BoolFunction(0)
    v4 = BoolFunction(1)
    v5 = BoolFunction(1)
    v6 = BoolFunction(1)
    v7 = BoolFunction(0)
    v8 = BoolFunction(1)
    l1_1 = BoolFunction(None, [v1,v2], Gate.AND)
    l1_2 = BoolFunction(None, [v3,v4], Gate.OR)
    l1_3 = BoolFunction(None, [v5,v6], Gate.AND)
    l1_4 = BoolFunction(None, [v7,v8], Gate.OR)
    l2_1 = BoolFunction(None, [l1_1,l1_2], Gate.AND)
    l2_2 = BoolFunction(None, [l1_3,l1_4], Gate.AND)
    l3_1 = BoolFunction(None, [l2_1,l2_2], Gate.AND)
    return l3_1

rootNode = exampleFunction()

def generate_binary_combinations(n):
    return itertools.product([0, 1], repeat=n)



def evaluateFunctionNaively(rootNode):
    vars = rootNode.getVars()
    data = list(generate_binary_combinations(len(vars)))
    functionEvaluation = {}
    
    for dataPoint in data:
        for i,var in enumerate(vars):
            print(i, var)
            var.value = dataPoint[i]
        functionEvaluation[dataPoint] = var.value
        
    print(len(functionEvaluation))

def evaluateFunctionOptimally():
    pass

evaluateFunctionNaively(rootNode)