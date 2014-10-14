#include <stdio.h>
#include <stdlib.h>

void merge(int* nums, int left, int mid, int right){
    // O(n) space needed for tmp array
	int tmp[right-left+1];
	int ind = 0, lpos = left, rpos = mid+1;
	
	// copy over the smallest of the first element
	//	on the left and the first on the right
	while(lpos<=mid && rpos<=right){
		if(nums[lpos]<=nums[rpos]){
			tmp[ind++]=nums[lpos++];
		}
		else{
			tmp[ind++]=nums[rpos++];
		}
	}

	// when all the elements on the left have been 
	//	copied over, copy over the ones left over
	// 	on the right
	while(lpos<=mid){
		tmp[ind++]=nums[lpos++];
	}
	while(rpos<=right){
		tmp[ind++]=nums[rpos++];
	}
	
	// copy back over to the original array
	int i;
	for(i=0; i<ind; i++)
	{
		nums[i+left]=tmp[i];
	}
}

// Merge sort
void merge_sort(int* nums, int left, int right){
	int mid = left + (right-left)/2;
	if(left<right)
	{
		merge_sort(nums, left, mid);
		merge_sort(nums, mid+1, right);
		merge(nums, left, mid, right);
	}
}

void quick_sort(int* a, int length){
    // base case: 1 element
    if(length < 2) return;
    // select the midpoint as pivot
    int pivot = a[length/2];
    int* left = a;
    int* right = a + length - 1;
    while(left <= right){
        if(*left < pivot) left++;
        else{
            if(*right > pivot) right--;
            else{ // swap
                int tmp = *(left); 
                *(left) = *(right);
                *(right) = tmp;
                left++;
                right--;
            }
        }
        
    }
    quick_sort(a, right - a + 1);
    quick_sort(left, a + length - left);
}

int main(void){
	// int arr[7] = {100, 2,5,1,6,3,7};
    int arr[7] = {'a', 'd', 'b', 'e', 'f', 'g', 'a'};
    int size = sizeof(arr)/sizeof(arr[0]);
    printf("%zu\n", sizeof(arr)/sizeof(arr[0]));
	quick_sort(arr, sizeof(arr)/sizeof(arr[0]));
	int i;
	for(i=0; i<size; i++)
		printf("Merge sort: %c\n", arr[i]);
} 
