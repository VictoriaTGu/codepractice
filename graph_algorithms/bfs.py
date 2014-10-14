def breadthFirstSearch(root):
    Q = Queue.Queue()
    visited = [root]
    Q.put(root)
    while not Q.empty():
        current = Q.get()
        current.printout()
        children = current.getChildren()
        for child in children:
            if child not in visited:
                visited.append(child)
                Q.put(child)    
        
