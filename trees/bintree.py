class node:
	left, right, data = None, None, 0
	def __init__(self, data):
		self.left = None
		self.right = None
		self.data = data

class btree:
	def __init__(self):
		self.root = None

	def addNode(self, data):
		return node(data)

	def insert(self, root, data):
		if(root == None):
			root = self.addNode(data)
			return root
		else:
			if data <= root.data:
				root.left = self.insert(root.left, data)
			else:
				root.right = self.insert(root.right, data)
			return root
	def lookup(self, root, target):
		if root == None:
			return 0
		else:
			if root.data == target:
				return 1
			else:
				if root.data <= target:
					return self.lookup(root.left, target)
				else:
					return self.lookup(root.right, target)
	def top(self, root, x):
		if root == None:
			return max
		else:
			max1 = self.top(root.left, x)
			max2 = self.top(root.right, x)
			lst = [root.data, max1, max2]
			return max(lst)

	def toptwo(self, root, max1, max2):
		if root == None:
			return (max1, max2)
		else:
			(a1, a2) = self.toptwo(root.left, max1, max2)
			if root.data > max2:
				if root.data > max1:
					max2 = max1
					max1 = root.data
				else:
					max2 = root.data
			(b1, b2) = self.toptwo(root.right, max1, max2)

			return (max1, max2)
def main():
	BT = btree()
	root = BT.addNode(10)
	#print BT.lookup(root, 0)
	print (BT.top(root, 0))
		
if __name__ == "__main__":
	main()
	
