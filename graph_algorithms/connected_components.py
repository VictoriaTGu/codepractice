#!/usr/bin/env python
import numpy as np
import Queue

class Vertex:
    def __init__(self, key):
        self.id = key
        self.neighbors = []
    def getID(self):
        return self.id
    def addNeighbor(self, neighbor):
        if neighbor != None:
            self.neighbors.append(neighbor)
    def getNeighbors(self):
        return self.neighbors
    def __str__(self):
        return str(self.id) + ' connected to ' + \
            str([neighbor.id for neighbor in self.neighbors])
    def __eq__(self, other):
        return self.id == other.id

class Graph:
    def __init__(self):
        self.vertex_list = {} 
        self.num_vertices = 0
    def isEmpty(self):
        return self.num_vertices <= 0
    # the key is the (i,j) position in the input array
    def addVertex(self, key):
        # vertex already exists
        if key in self.vertex_list:
            return
        new_vertex = Vertex(key)
        self.vertex_list[key] = new_vertex
        self.num_vertices += 1
    # pick a pseudo-random starting point for traversing graph
    def randomVertex(self):
        if self.isEmpty():
            return None
        key = self.vertex_list.keys()[0]	
        return self.vertex_list[key]
    def getVertex(self, key):
        if key in self.vertex_list:
            return self.vertex_list[key]
        return None
    # add two vertices and an edge between them
    def addEdge(self, key1, key2):
        self.addVertex(key1)
        self.addVertex(key2)
        self.getVertex(key1).addNeighbor(self.getVertex(key2))
    # input: list of keys of nodes to be deleted
    def deleteVertices(self, key_list):
        for key in key_list:
            if key in self.vertex_list:
                del self.vertex_list[key]
                self.num_vertices -= 1  
    def show(self):
        for vertex in self.vertex_list:
            print self.vertex_list[vertex]

# returns the set of nodes visited in BFS
def breadthFirstSearch(graph, start_node):
    # FIFO queue
    Q = Queue.Queue()
    # set of visited nodes
    visited = [start_node]
    Q.put(start_node)
    while not Q.empty():
        current_node = Q.get()
        neighbors = current_node.getNeighbors()
        for neighbor in neighbors:
            if neighbor not in visited:
                visited.append(neighbor)
                Q.put(neighbor)
    visited_keys = map(lambda vertex: vertex.getID(), visited)
    return visited_keys
		
# checks whether indices are within the bounds of a square array
def inArray(i, j, size):
    if i < 0 or j < 0:
        return False
    if i >= size or j >= size:
        return False
    return True

# dictionary mapping from neighbor to elevation value 
def getArrayNeighbors(array, i, j, size):
    neighbors = {} 
    if inArray(i, j+1, size):
        neighbors[i,j+1] = array[i][j+1]
    if inArray(i-1, j, size):
        neighbors[i-1,j] = array[i-1][j]
    if inArray(i, j-1, size):
        neighbors[i,j-1] = array[i][j-1]
    if inArray(i+1, j, size):
        neighbors[i+1,j] = array[i+1][j]
    return neighbors

# out of the four (or fewer) neighbors of a plot of land,
#   return the one with the lowest elevation (the sink)
def getSink(array, i, j, size):
    neighbors = getArrayNeighbors(array, i, j, size)
    current_min = array[i][j]
    min_index = (i,j)
    # return the key of the neighbor with the min value
    for key in neighbors:
        if neighbors[key] < current_min:
            current_min = neighbors[key]
            min_index = key
    return min_index

# input: square array of elevation data with dimensions (size x size)
# output: sizes of basins (connected components) in decreasing order
def findConnectedComponents(array, size):
    graph = Graph()
    # create a graph where A and B are connected if A is a sink for B or
    #   B is a sink for A
    for row_num in range(size):
        for col_num in range(size):
            current_vertex = (row_num, col_num)
            graph.addVertex(current_vertex)
            flow_to = getSink(array, row_num, col_num, size)
            if current_vertex != flow_to:
                # add edges both ways
                graph.addEdge(current_vertex, flow_to)
                graph.addEdge(flow_to, current_vertex)
    size_of_components = []
    # find connected components and delete them until graph is empty
    while not graph.isEmpty():
        start = graph.randomVertex()
        vertex_list = breadthFirstSearch(graph, start)
        size_of_components.append(len(vertex_list))
        graph.deleteVertices(vertex_list)
    return sorted(size_of_components, reverse=True)
			
def main():
    # unit tests
    array = [[1,5,2],[2,4,7],[3,6,9]]
    size = 3
    print findConnectedComponents(array, size) == [7,2]

    array = [[3,6,9],[2,4,7],[1,5,2]]
    size = 3
    print findConnectedComponents(array, size) == [7,2]

    array = [[10]]
    size = 1
    print findConnectedComponents(array, size) == [1]

    array = [[1,0,2,5,8], [2,3,4,7,9], [3,5,7,8,9], [1,2,5,4,3], [3,3,5,2,1]]
    size = 5
    print findConnectedComponents(array, size) == [11, 7, 7]

    array = [[0,2,1,3],[2,1,0,4],[3,3,3,3],[5,5,2,1]]
    size = 4
    print findConnectedComponents(array, size) == [7,5,4]

if __name__ == "__main__":
	main()
