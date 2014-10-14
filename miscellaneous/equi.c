#include <stdlib.h>
#include <stdio.h>

int equi(int arr[], int n)
{
  int i, j;
  int leftsum, rightsum;
 
  /* Check for indexes one by one until an equilibrium
    index is found */
  for ( i = 0; i < n; ++i)
  {
    leftsum = 0;  // initialize left sum for current index i
    rightsum = 0; // initialize right sum for current index i
 
    /* get left sum */
    for ( j = 0; j < i; j++)
      leftsum  += arr[j];
 
    /* get right sum */
    for( j = i+1; j < n; j++)
      rightsum += arr[j];
 
    /* if leftsum and rightsum are same, then we are done */
    if (leftsum == rightsum)
      return i;
    }
 
  /* return -1 if no equilibrium index is found */
  return -1;
}

// more efficient solution
int equilibrium(int arr[], int n)
{
   int sum = 0;      // initialize sum of whole array
   int leftsum = 0; // initialize leftsum
   int i;
 
   /* Find sum of the whole array */
   for (i = 0; i < n; i++)
        sum += arr[i];
 
   for( i = 0; i < n; i++)
   {
      sum -= arr[i]; // sum is now right sum for index i
 
      if(leftsum == sum)
        return i;
 
      leftsum += arr[i];
   }
 
    /* If no equilibrium index found, then return 0 */
    return -1;
} 

int main(void){
	int arr[6]={-7, 1, 5, -4, 3, 0};
	int sol = equilibrium(arr, 6);
	printf("%d\n", sol);
	return 0;
}
