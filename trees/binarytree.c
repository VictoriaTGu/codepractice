/*
    BST lookup: recursive
    BST lookup: iterative
    Height of BT: recursive
    Least Common Ancestor of two nodes
    Top two nodes in an unsorted binary tree
        - see python recursive implementation
        - can do BFS iteratively and keep track
            of two two nodes
    Mirror a binary tree
*/
#include <stdio.h>
#include <stdlib.h>

typedef struct Node{
    int data;
    struct Node* left;
    struct Node* right;
} Node;

int lookup_recursive(Node* head, int n){
    if(!head) return 0;
    int curr_val = head -> data;
    if(curr_val == n) return 1;
    if(curr_val < n) {
        lookup_recursive(head->right, n);
    } else{
        lookup_recursive(head->left,n);
    }
}

// lookup is a O(log(n)) operation in a balanced
//  binary search tree
int lookup_iterative(Node* head, int n){
    while(head){
        int curr_val = head -> data;
        if(curr_val == n) return 1;
        if(curr_val < n){
            head = head -> right;
        } else{ // curr_val > n
            head = head -> left;
        }
    }
    return 0;
}

int max(x, y){
    if(x <= y){
        return y;
    }
    else{
        return x;
    }
}
int min(x, y){
    if(x >= y){
        return y;
    }
    else{
        return x;
    }
}

int height_of_tree(Node* head){
    if(!head) return 0;
    return 1 + max(height_of_tree(head->left), height_of_tree(head->right));
}

// assumes a BST
int least_common_ancestor(Node* head, int x, int y){
    while(head){
        int max_val = max(x,y);
        int min_val = min(x,y);
        int curr_val = head -> data;
        if(curr_val >= min_val && curr_val <= max_val){
            return curr_val;
        }
        if (curr_val > max_val){
            head = head -> left;
        } else{ // curr_val < min_val
            head = head -> right;
        }
    }
    return NULL;
}

/*void top_two_nodes(Node* head){
    if(!(head->left)
    int top_two_left[2] = top_two_nodes(head->left);
    int top_two_right[2] = top_two_nodes(head->right);
}*/

void print_tree(Node* head){
    if(!head) return;
    print_tree(head->left);
    printf("%d\n", head->data);
    print_tree(head->right);
}

void mirror(Node* head){
    if(!head) return;
    Node* tmp = head->left;
    head->left = head->right;
    head->right = tmp;
    mirror(head->left);
    mirror(head->right);
}

int main(void){
    Node one = {1, NULL, NULL};
    Node four = {4, NULL, NULL};
    Node seven = {7, NULL, NULL};
    Node twelve = {12, NULL, NULL};
    Node three = {3, &one, &four};
    Node nine = {9, &seven, &twelve};
    Node five = {5, &three, &nine};
    mirror(&five);
    mirror(&five);
    print_tree(&five);
}
