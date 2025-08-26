def compress(lst: str) -> str:
	"""
	Compresses a string using run-length encoding.
	For example, 'aabccccdd' -> '2a1b4c2d'.

	Args:
		lst (str): Input string to compress.
	Returns:
		str: Compressed string.
	"""
	if not isinstance(lst, str):
		raise TypeError("Input must be a string.")
	length = len(lst)
	if length < 1:
		return ""
	output = []
	prev = lst[0]
	counter = 1
	for i in range(1, length):
		if lst[i] == prev:
			counter += 1
		else:
			output.append(str(counter) + prev)
			counter = 1
			prev = lst[i]
	output.append(str(counter) + prev)
	return ''.join(output)
