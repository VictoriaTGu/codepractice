class Node:
    def __init__(self, data, left, right):
        self.data = data
        self.left = left
        self.right = right

def top_two_nodes(head):
    if head.left == None and head.right == None:
        return [head.data,0]
    return sorted(top_two_nodes(head.left) + top_two_nodes(head.right), reverse=True)[:2]

def main():
    twelve = Node(12, None, None)
    one = Node(100, None, None)
    four = Node(4, None, None)
    ten = Node(10, None, None)
    three = Node(3, one, four)
    nine = Node(9, ten, twelve)
    five = Node(5, three, nine)
    print top_two_nodes(five)

if __name__ == "__main__":
    main()
