/*
 * Testing bitwise operations
 */
#include <stdio.h>
#include <stdlib.h>


/* Bitwise AND/OR will take the logical AND/OR of the
 * bits of the number in binary 
 * Imagine a row of machines 1010001, where 1 indicates
 * that the machine is being used, 0 means it's free 
 */
int is_in_use(int machine_num)
{
	// Assume that one of the machines is in use
	char in_use = 9;
	// machine_num is the power of 2
	return in_use & ((1 << machine_num)+1);
}

// Bitwise XOR
int flip_use_state(int machine_num)
{
	char in_use = 9;

	// flip the state of a particular machine on or off
	return in_use ^ 1 << machine_num;
}

/* [var] << [n] will multiply the var by a power of 2^n
 * [var] >> [n] will divide the var by a power of 2^n 
 */ 
int power_2(int n, int power)
{
	return n >> power;
}
int
main(void)
{
	int n = 4;
	n = power_2(n, 1);
	printf("%d\n", n);
	printf("%d\n", is_in_use(3));
	printf("%d\n", flip_use_state(3));
}
