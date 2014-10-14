#include <stdio.h>
#include <stdlib.h>

typedef struct Node{
    struct Node *next;
    int data;
} Node;

void traverse(Node* current){
    while(current != NULL){
        printf("%d\n", current->data);
        current = current -> next;
    }
}

// find the nth to last node
Node* nthToLast(Node* head, int n){
    Node* prev = head;
    Node* current = head;
    // move current pointer n places forward
    for(int i=0; i<n; i++){
        if(current != NULL){
            current = current -> next;
        } else {
            return NULL;
        }
    }
    while(current != NULL){
        prev = prev -> next;
        current = current -> next;
    } 
    return prev;
}

Node* reverse(Node* head){
    Node* prev = NULL;
    Node* current = head;
    Node* oneahead = current -> next;
    while(current != NULL){
        printf("%d\n", current->data);
        current -> next = prev; 
        prev = current;
        current = oneahead;
        if(oneahead != NULL){ 
            oneahead = oneahead -> next;
        }
    }
    printf("%s\n", "success");
    return prev;
}

Node* deleteNode(Node* root, int n){
    Node* prev = NULL;
    Node* current = root;
    while(current != NULL){
        if(current -> data == n){
            // deleting the first element of the list
            if(prev == NULL){
                Node* tmp = current -> next;
                free(current);
                return tmp; 
            }
            prev -> next = current -> next;
            free(current);
            return root;
        }
        // keep traversing
        else{
            prev = current;
            current = current -> next;
        }
    }
    return root;
}

// place new node in the right position
Node* newNode(Node* root, int n){
    Node* prev = NULL;
    Node* current = root;
    // traverse until we encounter a node greater than n
    //  or we hit the end of the list
    while(current != NULL && current->data <= n){
        prev = current;
        current = current -> next;
    }
    Node* newNode = malloc(sizeof(Node));
    newNode -> data = n;
    newNode -> next = current;
    if(prev != NULL){
        prev -> next = newNode; 
        return root;
    }
    return newNode;
    
}


int main(void){
    // Populate the linked list with nodes for integers 10-15
    Node* root;
    root = malloc(sizeof( Node));
    if(root==NULL)
        return 1;
    Node* conductor;
    conductor=root;
    int i;
    for(i=0; i<6; i++)
    {
        conductor -> data = 10 + i;
        if(i<5)
        {
            conductor -> next = malloc(sizeof( Node));
            if(conductor -> next == NULL) return 1;
            conductor = conductor -> next;
        }
        else
        {
            conductor -> next = NULL;
        }
    }

    // Node* new;

    // Add a node to the appropriate position in the linked list
    Node* new = newNode(root, 14);

    // Delete another node
    new = deleteNode(new, 12);
    new = deleteNode(new, 10);

    // new = reverse(new);

    // Free the list
    traverse(new);
    // Node* head = reverse(root);
    // traverse(head);
    Node* nth = nthToLast(new, 1);
    printf("\n");
    if(nth != NULL) printf("%d\n", nth->data);
    

}
