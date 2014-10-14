/*
 * Doubly-Linked list implementation and operations
 * 	traversal (and freeing)
 *	reversal
 *	adding a node (in order from least to greatest)
 *	deleting a node
 *
 */
#include <stdio.h>
#include <stdlib.h>

struct Node{
	int Data;
	struct Node *Next;
	struct Node *Prev;
};

// Traverse and free the list given a pointer to a starting node
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

/* Reverse the linked list given the pointer to the start node
struct Node* reverse(struct Node* conductor)
{
	// Temporary pointer for node immediately preceding the conductor
	struct Node* prev;
	prev = conductor;

	// Temporary pointer for node immediately following the conductor
	struct Node* tmp;

	conductor = conductor -> Next;

	prev -> Next = NULL;

	while(conductor != NULL)
	{
		tmp = conductor -> Next;
		conductor -> Next = prev;
		
		// shift conductor and prev over by one
		prev = conductor;
		conductor = tmp;	
	}
	
	return prev;
}*/

// Insert a new node in the correct position in the list
struct Node* newNode(struct Node* root, int n)
{
	// create the new node
	struct Node *new;
	new = malloc(sizeof(struct Node));
	new -> Data = n;
	
	// create conductor to traverse the list
	struct Node *conductor;
	conductor = root;

	// insert at the front of the list
	if(conductor -> Data > n){
		new -> Next = conductor;
		conductor -> Prev = new;
		return new;
	}

	// insert after the front of the list, before the end
	while(conductor-> Next != NULL)
	{
		if(conductor -> Data <= n){
			conductor = conductor -> Next;
		} 
		else{
			struct Node *prev;
			prev = conductor -> Prev;
			prev -> Next = new;
			new -> Prev = prev;
			new -> Next = conductor;
			conductor -> Prev = new;
			return root;
		}
	}

	// insert at the end of the list
	conductor -> Next = new;
	new -> Prev = conductor;
	new -> Next = NULL;
	return root;
}

/*
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
}*/

int
main(void){
	// Populate the linked list with nodes for integers 10-15
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
			struct Node* tmp;
			tmp = conductor;
			conductor = conductor -> Next;
			conductor -> Prev = tmp;
		}
		else
		{
			conductor -> Next = NULL;
		}
	}
	
	struct Node* new;
		
	// Add a node to the appropriate position in the linked list
	new = newNode(root, 11);
	
	// Delete another node
	//new = deleteNode(new, 12);
	
	//new = reverse(new);

	// Free the list
	traverse(new);
	
}
