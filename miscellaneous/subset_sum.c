
/*
 * Given an array of numbers and an integer n, find the number of ways elements 
 * of the array can sum up to n. O(n^(k-1) log n) implementation, with k being the
 * size of the initial array.
 *
 */

// Find all possible subsets of size subset_size that sum to x
int recurse(int arr[], arr_size, int x, int ways, int subset_size, int sum){
	for(i=0; i<arr_size, arr[i]<x; i++){
		if(subset_size==1){
			if(bin_search(arr, x-sum))
				ways+=1;
		}
		else{
			sum += arr[i];
			recurse(arr, arr_size, x, ways, subset_size-1, sum);
		}
	}
	return ways;
}

int main(void){	
	int i;
	
	int arr = (1,4,6,7,8,9,10,14,15,17);
		
	// size of the array
	int size=10;
	
	// integer seeking
	int x=25;
	
	// number of arrays that sum to x
	int ways=0;

	// look for all arrays from size 1 to the full size
	for( i=1; i < size, i++){
     		ways += recurse(arr, size, x, ways, i, 0);
	}
	print("%d\n", ways);
}
