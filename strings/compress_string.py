def compress (lst):
	output = ""
	length = len(lst)
	if length < 1:
		return output
	prev = lst[0]
	counter = 1
	for i in range(1, length):
		if lst[i] == prev:
			counter += 1
		else:
			output += str(counter) + prev
			counter = 1
			prev = lst[i]
	return output + str(counter) + prev

print compress("aabccccdd")
