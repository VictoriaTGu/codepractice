/* Given a long string, tests whether it contains a given substring
 * Does what StrStr.c does except with pointers
 * haystack is the long strong
 * needle is the substring
 */
#include <stdio.h>
#include <stdlib.h>

char* StrStr(char* haystack, char* needle) {
    for (;; ++haystack) {
        char* h = haystack;
        for (char* n = needle;; ++n, ++h) {
            //printf("%s\n", h);
	    if (!*n) return haystack;
            if (*h != *n) break;
        }
        if (!*h) return NULL;
    }
}

char* StrStr2(char* haystack, char* needle) {
	char* ptr;
	int len = 0;
	for(int i=0; haystack[i]!='\0'; i++)
	{
		for(int j=0;; j++)
		{
			if(haystack[i]!=needle[j])
				break;
			else
				len++;
			if(needle[j]=='\0')
				ptr = malloc(sizeof(char*));
				*ptr = haystack[i-len];
				//ptr = (char* )
				//printf("%c",haystack[i-len]);
				break;
		}
		
	}
	if(*ptr)
		return ptr;
	else
		return NULL;
}
int main(void)
{
        char* hay = "Do Re Mi Fa";
        char* needle = "Mi";
        char* result = StrStr(hay, needle);
        if(result!=NULL)
		printf("%s\n", result);
}
