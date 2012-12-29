#include <stdio.h>
#include <string.h>
 /* strstr */
 char *(StrStr)(const char *haystack, const char *needle)
 {
     size_t needlelen;
     /* Check for the null needle case.  */
     if (*needle == '\0')
         return (char *) haystack;
     needlelen = strlen(needle);
     for (; (haystack = strchr(haystack, *needle)) != NULL; haystack++)
         if (strncmp(haystack, needle, needlelen) == 0)
             return (char *) haystack;
     return NULL;
 }
int main(void)
{
	const char *hay = "Yo ho";
	const char *needle = "Yo";
	char* result = StrStr(hay, needle);
	printf("%d\n", *result);
}
