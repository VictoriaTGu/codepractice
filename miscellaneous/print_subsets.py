# Prints all subsets of a set, O(2^n) running time

def subsets(my_set):
    result = [[]]
    for x in my_set:
        result = result + [y + [x] for y in result]
        print result
    return result

def print_sets(arr):    
        for set in arr: 
                print ', '.join(set)

print_sets(subsets(['a','b','c','d']))
