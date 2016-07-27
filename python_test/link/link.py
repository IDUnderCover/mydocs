#!/usr/bin/env python
# -*- coding: utf8 -*-

class Node(object):
    
    def __init__(self, n_value=None, n_next=None):
        self.n_value = n_value
        self.n_next = n_next

    def __repr__(self):
        return '<Node value=%s>' % self.n_value

    __str__ = __repr__



class Link(object):
    
    def __init__(self, head=None):
        self.head = head or Node()
        self.tail = self.head

    def add_tail(self, node):
        self.tail.n_next = node
        self.tail = node
        
    def show(self):
        p = self.head
        while p:
            print p
            p = p.n_next

    def pop(self):
        if self.head.n_next:
            pop_node = self.head.n_next
            self.head = pop_node
            print 'pop node %s' % pop_node

    def reverse(self):
        pre = self.head
        cur = self.head.n_next
        while cur:
            nxt = cur.n_next  
            cur.n_next = pre 
            pre = cur
            cur = nxt
        self.head.n_next = None
        self.head, self.tail = pre, self.head 
        
        

if __name__ == '__main__':
    head = Link(Node(1))
    head.add_tail(Node(2))
    head.add_tail(Node(3))
    head.add_tail(Node(4))
    head.show()
    print '======================='
    head.pop() 
    head.show()
    print '======================='
    head.reverse()
    head.show()
