/*
 * Hash table implementation (adopted from literateprograms.org)
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef size_t hash_size;

struct hashnode{
	char* key;
	void* data;
	struct hashnode* next;
};

typedef struct hashtbl{
	hash_size size;
	
	// nodes is a pointer to an array of pointers to the first element 
	//	of a linked list
	struct hashnode **nodes;
	
	hash_size (*hashfunc)(const char *);
} HASHTBL;

HASHTBL* hashtbl_create(hash_size size, hash_size(*hashfunct)(const char *));
void hashtbl_free(HASHTBL *hashtbl);
int hashtbl_insert(HASHTBL *hashtbl, const char *key, void *data);
//int hashtbl_remove(HASHTBL *hashtbl, const char *key);
void *hashtbl_get(HASHTBL *hashtbl, const char *key);
//int hashtbl_resize(HASHTBL *hashtbl, hash_size size);

// implementation of strdup()
static char *mystrdup(const char *s)
{
	char *b;
	if(!(b=malloc(strlen(s)+1))) return NULL;
	strcpy(b, s);
	return b;
}

// default hash function adds together the key's ASCII values
static hash_size def_hashfunc(const char *key)
{
	hash_size hash=0;
	
	while(*key) hash+=(unsigned char)*key++;

	return hash;
}

// free the hash table
void hashtbl_free(HASHTBL *hashtbl){
	hash_size n;
	struct hashnode *node, *oldnode;
	for(n=0; n < hashtbl->size; ++n){
		node = hashtbl->nodes[n];
		while(node){
			oldnode=node;
			node=node->next;
			free(oldnode);
		}
	}
	free(hashtbl->nodes);
	free(hashtbl);
		
}

int hashtbl_insert(HASHTBL *hashtbl, const char* key, void* data){
	hash_size hash = hashtbl->hashfunc(key) % hashtbl->size;
	struct hashnode *node;
	node = hashtbl->nodes[hash];
	while(node){
		if(strcmp(node->key, key)==0){
			node->data=data;
			return 0;
		}
		node=node->next;
	}

	// if key is not found, insert node at beginning of the list
	node = malloc(sizeof(struct hashnode));
	
	// copy the key into the new node
	if(!(node->key=mystrdup(key))){
		free(node);
		return -1;
	}
	node -> data = data;
	node -> next = hashtbl->nodes[hash];
	hashtbl->nodes[hash]=node;
	return 0;
}

// searches for a key and returns its data value
void* hashtbl_get(HASHTBL *hashtbl, const char* key){

	// compute the hash value for the key
	hash_size hash = hashtbl -> hashfunc(key) % (hashtbl -> size);
	
	// access the linked list for that hash value
	struct hashnode *node;
	node = hashtbl->nodes[hash];
	
	// if key is found, return data value
	while(node){
		if(strcmp(key, node->key)==0)
			return node -> data;
		node = node -> next;
	}
	return NULL;
}

HASHTBL* hashtbl_create(hash_size size, hash_size (*hashfunc)(const char *)){
	HASHTBL *hashtbl;
	hashtbl = malloc(sizeof(HASHTBL));
	if(hashtbl==NULL)
		return NULL;

	hashtbl -> nodes = calloc(size, sizeof(struct hashnode*));
	if(hashtbl->nodes == NULL){
		free(hashtbl);
		return NULL;
	}

	hashtbl -> size = size;

	if(hashfunc)
		hashtbl -> hashfunc = hashfunc;
	else
		hashtbl -> hashfunc = def_hashfunc;
	
	return hashtbl;
}
int main(void){
	HASHTBL *hashtbl;
	if(!(hashtbl=hashtbl_create(16, NULL))){
		fprintf(stderr, "Error: hashtbl_create() failed\n");
		exit(EXIT_FAILURE);
	}

	hashtbl_insert(hashtbl, "Sports", "Tennis");
	hashtbl_insert(hashtbl, "Sports", "Football");
	const char *str = hashtbl_get(hashtbl, "Sports");
	printf("Inserted: %s\n", str);
	
	return 0;
}
