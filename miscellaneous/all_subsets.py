import copy

def all_subsets(s):
    lst = [[]]
    for character in s:
        duplicate_lst = copy.deepcopy(lst)
        duplicate_lst = [sublist + [character] for sublist in duplicate_lst]
        lst.extend(duplicate_lst)
    return lst

print all_subsets([1,2,3])
