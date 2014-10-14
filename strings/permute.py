def permute(s):
    lst = []
    if s == "":
	    return [""]
    for (index, character) in enumerate(s):
        lst.extend([character + ending for ending in permute(s[:index]+ s[index+1:])])
    return lst

string_to_permute = "abcd"
print "Hello"
for item in permute(string_to_permute):
    print item
