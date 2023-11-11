import random
from function import BoolFunction, Gate

def get_random_gate():
    randInt = random.randint(0,1)
    return Gate.AND if randInt else Gate.OR

def generate_random_bool_function(depth = 3, minK = 2, maxK=2):
    if depth == 0:
        return BoolFunction()
    
    rootNode = BoolFunction(None, [], gate = get_random_gate())
    childrenCount = random.randint(minK, maxK)
    for i in range(childrenCount):
        rootNode.addChild(generate_random_bool_function(depth - 1, minK, maxK))
    return rootNode
    

