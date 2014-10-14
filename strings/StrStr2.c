/* 
 *Given a long string, tests whether it contains a given substring
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

int main(void)
{
        char* hay = "Do Re Mi Fa";
        char* needle = "Mi";
        char* result = StrStr(hay, needle);
        if(result!=NULL)
		printf("%s\n", result);
}
