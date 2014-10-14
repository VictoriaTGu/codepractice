#!/usr/bin/env python

def merge(list1, list2):
    merged_lst = []
    counter1 = 0
    counter2 = 0
    len1 = len(list1)
    len2 = len(list2)
    while counter1<len1 and counter2<len2:
        if list1[counter1] <= list2[counter2]:
            merged_lst.append(list1[counter1])
            counter1 += 1
        elif list1[counter1] > list2[counter2]:
            merged_lst.append(list2[counter2])
            counter2 += 1
    if counter1 < len1:
        return merged_lst + list1[counter1:]
    elif counter2 < len2: 
        return merged_lst + list2[counter2:]
    return merged_lst

def mergesort(lst):
    if len(lst) <= 1:
        return lst
    mid = (len(lst)) / 2 
    l = mergesort(lst[:mid])
    r = mergesort(lst[mid:])
    return merge(l, r)
    

def main():
    lst1 = [1,2,4,7,8]
    lst2 = [5,7,9,10]
    print merge(lst1, lst2)
    print merge(lst1, [])
    print mergesort([7,4,4,3,6,64])

if __name__ == "__main__":
    main()
