#!/usr/bin/python
# -*- coding: utf-8 -*_

import random
import math

def bubble_sort(lst):
    length = len(lst)
    for i in range(1, length ):
        for j in range(length - i):
            if lst[j] > lst[j+1]:
                lst[j], lst[j+1] = lst[j+1], lst[j]
    print(lst)

def select_sort(lst):
    length = len(lst)
    for i in range(length - 1):
        for j in range(i,length):
            if lst[i] > lst[j]:
                lst[j], lst[i] = lst[i], lst[j]
    print(lst)

def insertion_sort(lst):
    for p in range(1, len(lst)):
        tmp = lst[p]
        j = p
        while j > 0 and lst[j-1] > tmp:
            lst[j] = lst[j-1]
            j = j - 1
        lst[j] = tmp
    print(lst)
        

# Hibbard [1,3,7,...,2^k - 1]
def shell_sort(lst):
    length = len(lst)
    inc = length / 2
    while inc > 0:
        i = inc
        while i < length:
            tmp = lst[i]
            j = i
            while j >=inc and lst[j-inc] > tmp :
                lst[j] = lst[j - inc]
                j = j - inc
            lst[j] = tmp
            i = i + 1
        inc = inc / 2
    print(lst)

def heapsort(lst):
    pass

def mergesort(lst):
    pass

def quicksort(lst,l,r):
    if l <  r:
        index = partition(lst, l ,r)
        quicksort(lst, 0 , index)
        quicksort(lst, index+1, r)


def partition(lst, l, r):
    left = l
    right = r
    # 以第一个数为基准
    val = lst[l]
    while left < right:
        # 从右向左寻找比val小的数
        while left < right and lst[right] >= val:
            right -= 1
            
        if left < right:
            lst[left] = lst[right]
            left += 1
        # 从左向右找比val大的数
        while left < right and lst[left] <= val:
            left += 1
        if left < right:
            lst[right] = lst[left]
            right -= 1
    lst[left] = val 
    return left
if __name__ == '__main__':
    lst = [1,3,4,6,5,2,2,3,4,9,4,6,8,2,0,-1]
    bubble_sort(lst)
    lst = [1,3,4,6,5,2,2,3,4,9,4,6,8,2,0,-1]
    select_sort(lst)
    lst = [1,3,4,6,5,2,2,3,4,9,4,6,8,2,0,-1]
    insertion_sort(lst)
    lst = [1,3,4,6,5,2,2,3,4,9,4,6,8,2,0,-1]
    shell_sort(lst)
    lst = [1,3,4,6,5,2,2,3,4,9,4,6,8,2,0,-1]
    quicksort(lst,0, len(lst)-1)
    print(lst)
