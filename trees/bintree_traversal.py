"""
    Three types of DFS traversal on binary trees:
        Pre-order
        In-Order
        Post-Order
    These can be done recursively, or iteratively using a stack
"""
import Queue

class Node:
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right
    def getData(self):
        return self.data
    def getLeft(self):
        return self.left
    def getRight(self):
        return self.right
    def printOut(self):
        print self.data

def createTree():
    left2 = Node(1)
    right2 = Node(4)
    left3 = Node(6)
    right3 = Node(9)
    left = Node(2, left2, right2)
    right = Node(7, left3, right3)
    root = Node(5, left, right)
    return root
    

# in order traversal
def traverse(root):
    if root == None:
        return
    traverse(root.getLeft())
    root.printOut()
    traverse(root.getRight())

def inorder_iter(root):
    S = Queue.LifoQueue()
    top = root
    while not S.empty() or top != None:
        if top != None:
            S.put(top)
            top = top.getLeft()
        else:
            top = S.get()
            top.printOut()
            top = top.getRight()

def preorder_iter(root):
    S = Queue.LifoQueue()
    top = root
    while top != None: 
        top.printOut()
        right = top.getRight()
        if right != None:
            S.put(right) 
        left = top.getLeft()
        if left != None:
            S.put(left)
        top = S.get()
    return

# this method is actually slightly better than wikipedia
def preorder_iter2(node):
    S = Queue.LifoQueue()
    S.put(node)
    while not S.empty():
        node = S.get()
        node.printOut()
        right = node.getRight()
        left = node.getLeft()
        if right != None:
            S.put(node.getRight())
        if left != None:
            S.put(node.getLeft())
        
def main():
    root = createTree()
    preorder_iter2(root)

if __name__ == "__main__":
    main() 
