/*
 * Linked list implementation and operations
 *
 */
#include <stdio.h>
#include <stdlib.h>

struct Node{
	int Data;
	struct Node *Next;
};

// Traverse and free the list given a starting node
void traverse(struct Node* current)
{
	while(current != NULL)
	{
		printf("%d\n", current -> Data);
		struct Node* tmp;
		tmp = current;
		free(current);
		current = tmp -> Next;
	}
}

// Insert a new node to the front of the list
struct Node* newNode(struct Node* root, int n)
{
	struct Node* new;
	new = malloc(sizeof(struct Node));
	new -> Data = n;
	new -> Next = root;
	return new;
}

// Delete a node with a given integer value
struct Node* deleteNode(struct Node* root, int n)
{
	struct Node* conductor;
	struct Node* prev;
	prev = malloc(sizeof(struct Node));
	conductor = malloc(sizeof(struct Node));
	conductor = root;
	prev = conductor;
	while(conductor !=NULL)
	{
		if(n == (conductor -> Data))
		{
			if(conductor == prev)
			{
				root = conductor -> Next;
				conductor = conductor -> Next;
			}
			else
			{
				prev -> Next = conductor -> Next; 
				conductor = conductor -> Next;
			}	
		}
		else
		{
			prev = conductor; 
			conductor = conductor -> Next;
		}
	}
	return root;
}

int
main(void){
	// Popoulate the linked list
	struct Node* root;
	root = malloc(sizeof(struct Node));
	if(root==NULL)
		return 1;
	struct Node* conductor;
	conductor=root;
	int i;
	for(i=0; i<6; i++)
	{
		conductor -> Data = 10 + i;
		if(i<5)
		{
			conductor -> Next = malloc(sizeof(struct Node));
			conductor = conductor -> Next;
		}
		else
		{
			conductor -> Next = NULL;
		}
	}
	
	struct Node* new;
	struct Node* new2;
	
	// Add a node to the front of the linked list
	new = newNode(root, 5);
	
	// Delete another node
	new2 = deleteNode(new, 10);
	
	// Free the list
	traverse(new2);
}
