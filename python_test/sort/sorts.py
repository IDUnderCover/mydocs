#!/usr/bin/python
# -*- coding: utf-8 -*_

import random
import math

def bubble_sort(lst):
    length = len(lst)
    for i in range(1, length ):
        for j in range(length - i):
            if lst[j] > lst[j+1]:
                tmp = lst[j]
                lst[j] = lst[j+1]
                lst[j+1] = tmp
    print(lst)

def select_sort(lst):
    length = len(lst)
    for i in range(length - 1):
        for j in range(i,length):
            if lst[i] > lst[j]:
                tmp = lst[i]
                lst[i] = lst[j]
                lst[j] = tmp
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

if __name__ == '__main__':
    lst = [1,3,4,6,5,2,2,3,4,9,4,6,8,2,0,-1]
    bubble_sort(lst)
    lst = [1,3,4,6,5,2,2,3,4,9,4,6,8,2,0,-1]
    select_sort(lst)
    lst = [1,3,4,6,5,2,2,3,4,9,4,6,8,2,0,-1]
    insertion_sort(lst)
    lst = [1,3,4,6,5,2,2,3,4,9,4,6,8,2,0,-1]
    shell_sort(lst)
