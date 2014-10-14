void inOrder(Node* root, int n) {
    int counter = 0;
    Node* current = root;
    Node* parent = root;
    while (counter < n){
        arr = nextLargest(current, parent);
        current = arr[0];
        parent = arr[1];
        operation(current);
        counter += 1;
    }
}

void operation(struct* Node node){
    printf "%d" % (node -> data);
}
     4
   3   5
 2   
1  2.5
  2.2


struct** Node nextLargest(struct* Node node, struct* Node parent){
    if (node -> left && node -> left -> visited = false){
        parent = node;
        return nextLargest(node -> left, parent);
    }
    if (node -> visited = false){
        node -> visited = true;
        return [node, parent];
    }
    
    if (node -> right && node -> right -> visited = false){
        parent = node;
        return nextLargest(node -> right, parent);
    }
    if (parent){
        return nextLargest(parent);
    }
}
