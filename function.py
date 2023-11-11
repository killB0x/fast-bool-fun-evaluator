from enum import Enum
import itertools
import math

class Gate(Enum):
    AND = "and"
    OR = "or"
    
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
        self.value = self.gateOperator(childrenValues)
        return self.gateOperator(childrenValues)
    
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
        
def functionExample()
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

rootNode = functionExample()

def generate_binary_combinations(n):
    return itertools.product([0, 1], repeat=n)



def evaluateFunctionNaively(rootNode):
    vars = rootNode.getVars()
    data = list(generate_binary_combinations(len(vars)))
    functionEnumeration = {}
    
    for dataPoint in data:
        for i,var in enumerate(vars):
            var.value = dataPoint[i]
        functionEnumeration[''.join(map(str, dataPoint))] = rootNode.evaluate()
        
    return functionEnumeration

def generate_gray_code_with_changed_bit_indices(n):
    result = []
    previous_gray = 0  # Initialize with the first Gray code value
    for i in range(0, 2**n):
        current_gray = i ^ (i >> 1)
        if i == 0:
            changed_bit_index = None  # No bit changed for the first element
        else:
            changed_bit = previous_gray ^ current_gray
            changed_bit_index = (changed_bit & -changed_bit).bit_length() - 1
        result.append((format(current_gray, f'0{n}b'), None if changed_bit_index == None else n - changed_bit_index - 1))
        previous_gray = current_gray  # Update previous_gray for the next iteration
    return result

def evaluateFunctionOptimally(rootNode):
    vars = rootNode.getVars()
    data = generate_gray_code_with_changed_bit_indices(len(vars))
    functionEnumeration = {}
    for dataPoint,changedBit in data:
        if changedBit == None:
            for var in vars:
                var.value = 0
                functionEnumeration[dataPoint] = 0
                rootNode.evaluate()
        else:
            vars[changedBit].value = not vars[changedBit].value
            vars[changedBit].propagateChange()
            functionEnumeration[dataPoint] = rootNode.value
                
    return functionEnumeration

data1 = evaluateFunctionNaively(rootNode)
data2 = evaluateFunctionOptimally(rootNode)

for key,val in data1.items():
    print(data1[key], data2[key], key)
    assert(data1[key] == data2[key])