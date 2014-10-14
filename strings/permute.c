#include <stdlib.h>
#include <stdio.h>

/*
 * Prints all permutations of a string in O(n!) running time
 */

/* Function to swap values at two pointers */
void swap (char *x, char *y)
{
	char temp;
	temp = *x;
	*x = *y;
	*y = temp;
}

// check for duplicates
int check(char *arr,int i,int j)
{
	if(i==j)
		return 1;
	for(;i<j;i++){
		if(arr[i]==arr[j])
		{
			printf("0000000 %s\n", arr);
			return 0;
		}
	}
	return 1;
}

/* Function to print permutations of string
This function takes three parameters:
1. String
2. Starting index of the string
3. Ending index of the string. 
Every call of permute leaves the string unchanged 
This has an O(n * n!) running time, which is 
the size of the output. */
void permute(char *a, int start, int end)
{
	int j;
	if (start == end)
		printf("%s\n", a);
	else{
		for (j = start; j <= end; j++){
			printf("For loop: Start %c, j: %d\n", *(a+start), j);
			if(check(a,start,j)){
				
				//printf("Swap %c with %c\n", *(a+start), *(a+j));
				// swap two letters
				swap((a+start), (a+j));
				// recursive call on the tail of the string
				permute(a, start+1, end);

				// swap the same letters back
				//printf("Back Swap %c with %c\n", *(a+start), *(a+j));
				swap((a+start), (a+j));

			} //backtrack
		}
	}
}

/* Driver program to test above functions */
int main(){
	// only works on strings of length 5?
	char a[] = "abcde";
	permute(a, 0, 4);
	return 0;
}


