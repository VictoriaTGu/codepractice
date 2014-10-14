struct Node{
	struct leftChild* Node;
	struct rightChild* Node;
	int key;
};

void insert(int value)
{
    if(root == NULL)
        root = new Node(value);
    else
        insertHelper(root, value);
}
 
void insertHelper(Node* node, int value)
{
    if(value < node->key)
    {
        if(node->leftChild == NULL)
            node->leftChild = new Node(value);
        else
            insertHelper(node->leftChild, value);
    }
    else
    {
        if(node->rightChild == NULL)
            node->rightChild = new Node(value);
        else
            insertHelper(node->rightChild, value);
    }
}

int main(void{
	return 0;
}
