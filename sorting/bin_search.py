def binsearch_helper(lst, i, low, high):
    if (low <= high):
        med = low + (high - low) / 2
        if lst[med] == i:
            return med
        elif lst[med] > i:
            return binsearch_helper(lst, i, low, med - 1)
        else:
            return binsearch_helper(lst, i, med + 1, high)
    else:
        return None

def binsearch(lst, i):
    return binsearch_helper(lst, i, 0, len(lst)-1)
