/*
 * Reverses a string in place using pointers
 */
#include <stdio.h>
#include <string.h>

void reverse(char *str){
	char *end = str;
	char tmp;
	if(str)
	{
		while(*end)
			++end;
	}
	--end;
	while(str < end){
		printf("%d\n", str);
		tmp = *str;
		*str = *end;
		str++;
		*end-- = tmp;
	}
}

int
main(void){
	char *w = "abcdef";
	char target[strlen(w)+1];
	strcpy(target,w);
	reverse(target);
	printf("%s\n", target);
}
