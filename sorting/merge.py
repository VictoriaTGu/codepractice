from copy import deepcopy

# merge sort
def mergesort(lst):
	if len(lst) <= 1:
		return lst
	else:
		mid = len(lst) / 2
		left = lst[:mid]
		right = lst[mid:]
		left = mergesort(left)
		right = mergesort(right)
		result = merge(left, right)
		return result
		


# merge two sorted lists
def merge(left, right):
	result = []
	while len(left) > 0 and len(right) > 0:
		if left[0] <= right[0]:
			result.append(left[0])
			left = left[1:]
		elif right[0] < left[0]:
			result.append(right[0])
			right = right[1:]
	if len(left) > 0:
		result.extend(left)
	elif len(right) > 0:
		result.extend(right)
	return result

print merge([1,3,5],[2,4,6])
print mergesort([6,7,5,4,3,2,1])	
