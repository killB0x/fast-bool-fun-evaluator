import itertools
import time
from function_generator import generate_random_bool_function

def generate_binary_combinations(n):
    data = []
    for i in range(2 ** n):
        data.append(f"{i:0{n}b}")
        
    return data

def evaluateFunctionNaively(rootNode):
    vars = rootNode.getVars()
    data = list(generate_binary_combinations(len(vars)))
    functionEnumeration = {}
    
    start_time = time.time()
    for dataPoint in data:
        for i,var in enumerate(vars):
            var.value = int(dataPoint[i])
        functionEnumeration[dataPoint] = rootNode.evaluate()
    end_time = time.time() - start_time
    return functionEnumeration, end_time

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
    
    start_time = time.time()
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
    end_time = time.time() - start_time
    return functionEnumeration,end_time

def testCompleteBinaryTreeDepth():
    rootNode = generate_random_bool_function(3,2,3)
    print("Evaluated function " + str(rootNode))
    print("Generated function")
    print(str(len(rootNode.getVars())) + " variables")
    data_naive,time_naive = evaluateFunctionNaively(rootNode)
    print("Finished naive enumeration")
    data_optimal,time_optimal = evaluateFunctionOptimally(rootNode)
    print("Finished optimal evaluation")
    print("Time naive:", time_naive)
    print("Time optimal:", time_optimal)
    for key,val in data_optimal.items():
        # print(key, data_naive[key], data_optimal[key])
        assert(data_naive[key] == data_optimal[key])
    
testCompleteBinaryTreeDepth()
    
