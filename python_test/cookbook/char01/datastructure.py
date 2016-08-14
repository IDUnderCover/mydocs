#!/usr/bin/env python
# -*- coding: utf8 -*-

import heapq

class SimplePriorityQueue(object):
    
    def __init__(self):
        self.queue = []
        self.index = 0

    def push(self, item, priority):
        heapq.heappush(self.queue, (-priority, self.index, item))
        self.index += 1

    def pop(self):
        return heapq.headpop(self.queue)[-1]
        
