#!/usr/bin/env python
# coding=utf-8

from Queue import Queue    
import time

class Task(object):
    taskid = 0
    def __init__(self, target):
        Task.taskid += 1
        self.tid = Task.taskid
        self.target = target # target coroutine
        self.sendval = None # value to send

    def run(self):
        return self.target.send(self.sendval)


class Scheduler(object):
    def __init__(self):
        self.ready = Queue() # a Queue of tasks that are ready
        self.taskmap = {} # a dict that keeps track of all active tasks (each task has a unique task id)

    def new(self, target): # introduce a new task to the scheduler
        newtask = Task(target)
        self.taskmap[newtask.tid] = newtask
        self.schedule(newtask)
        return newtask.tid

    def schedule(self, task):
        self.ready.put(task) # put a task onto the ready queue

    def exit(self, task):
        print "Task %d terminated" % task.tid
        del self.taskmap[task.tid]

    def mainloop(self):
        while self.taskmap:
            task = self.ready.get()
            try:
                result = task.run()
            except StopIteration:
                self.exit(task)
                continue
            self.schedule(task)

def foo():
    for i in range(4):
        print "I'm foo"
        time.sleep(1)
        yield

def bar():
    for i in range(3): 
        print "I'm bar"
        time.sleep(1)
        yield

if __name__ == '__main__':
    sched = Scheduler()
    sched.new(foo())
    sched.new(bar())
    sched.mainloop()

