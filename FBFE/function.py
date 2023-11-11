from enum import Enum
import itertools
import math

class Gate(Enum):
    AND = "AND"
    OR = "OR"
    
class BoolFunction:
    def __init__(self, value=None, children=[], gate=None):
        self.value = value
        self.children = children
        self.gate = gate
        self.gateOperator = None
        self.parent = None
        self.trueChildren = 0
        
        if self.gate == Gate.AND:
            self.gateOperator = all
        elif self.gate == Gate.OR:
            self.gateOperator = any
        
        if self.children:
            for child in children:
                child.parent = self

    def __str__(self):
        stringFunction = ""
        if self.gate != None:
            stringFunction = self.gate.value + "("
            # print(len(self.children))
            for child in self.children:
                stringFunction += str(child) + ","
            
            stringFunction = stringFunction[:-1]
            stringFunction += ")"
        else:
            stringFunction = "Var"
        return stringFunction
    
    def addChild(self, child):
        self.children.append(child)
        child.parent = self
    
    def getVars(self):
        vars = []
        for child in self.children:
            if (child.children != []):
                vars.extend(child.getVars())
            else:
                vars.append(child)
        return vars
    
    def evaluate(self):
        for child in self.children:
            if (self.gate != None):
                self.value = self.gateOperator([self.value,child.evaluate()])
            else:
                return self.value
        if (self.gate == None):
            return self.value
        return self.value
    
    def propagateChange(self):
        if self.parent == None:
            return 
        
        if self.value:
            self.parent.trueChildren += 1
        else:
            self.parent.trueChildren -= 1
            
        prevVal = self.parent.value and 1
        self.parent.value = self.parent.trueChildren == len(self.parent.children) if self.parent.gate == Gate.AND else self.parent.trueChildren > 0 
        if self.parent.value == prevVal:
            return
        return self.parent.propagateChange()
        
# def functionExample():
#     v1 = BoolFunction(1)
#     v2 = BoolFunction(1)
#     v3 = BoolFunction(0)
#     v4 = BoolFunction(1)
#     v5 = BoolFunction(1)
#     v6 = BoolFunction(1)
#     v7 = BoolFunction(0)
#     v8 = BoolFunction(1)
#     l1_1 = BoolFunction(None, [v1,v2], Gate.AND)
#     l1_2 = BoolFunction(None, [v3,v4], Gate.OR)
#     l1_3 = BoolFunction(None, [v5,v6], Gate.AND)
#     l1_4 = BoolFunction(None, [v7,v8], Gate.OR)
#     l2_1 = BoolFunction(None, [l1_1,l1_2], Gate.AND)
#     l2_2 = BoolFunction(None, [l1_3,l1_4], Gate.AND)
#     l3_1 = BoolFunction(None, [l2_1,l2_2], Gate.AND)
#     return l3_1

# rootNode = functionExample()

# data1 = evaluateFunctionNaively(rootNode)
# data2 = evaluateFunctionOptimally(rootNode)

# for key,val in data1.items():
#     print(data1[key], data2[key], key)
#     assert(data1[key] == data2[key])