#include <stdio.h>
#include <string.h>

void anagram(char *str){
	char *end = str;
	if(str)
	{
		while(*end)
			++end;
	}
	--end;

	while(str < end)
	{
		if(*str != *end)
		{
			printf("%s\n", "No");
			break;
		}
		str++;
		end--;
	}
}
int main(void)
{
	anagram("ababa");
	return 0;
}
