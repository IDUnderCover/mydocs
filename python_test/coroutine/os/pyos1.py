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
        print "task %d running" % self.tid
        return self.target.send(self.sendval)

# base class
# all system operations will be implemented by inheriting from this class
class SystemCall(object):
    def handle(self):
        pass

class GetTid(SystemCall):
    def handle(self):
        self.task.sendval = self.task.tid
        self.sched.schedule(self.task)

class NewTask(SystemCall):
    def __init__(self, target):
        self.target = target
    def handle(self):
        tid = self.sched.new(self.target)
        self.task.sendval = tid
        self.sched.schedule(self.task)

class KillTask(SystemCall):
    def __init__(self, tid):
        self.tid = tid
    def handle(self):
        task = self.sched.taskmap.get(self.tid, None)
        if task:
            task.target.close()
            self.task.sendval = True
        else:
            self.task.sendval = False
        self.sched.schedule(self.task)

class WaitTask(SystemCall):
    def __init__(self, tid):
        self.tid= tid
    def handle(self):
        result = self.sched.waitforexit(self.task, self.tid)
        self.task.sendval = result
        # if waiting for a non-existent task, return immediately without waiting
        if not result:
            self.sched.schedule(self.task)

class ReadWait(SystemCall):
    def __init__(self, f):
        self.f = f
    def handle(self):
        fd = self.f.fileno()
        self.sched.waitforread(self.task, fd)

class WriteWait(SystemCall):
    def __init__(self, f):
        self.f = f
    def handle(self):
        fd = self.f.fileno()
        self.sched.waitforwrite(self.task, fd)

import select

class Scheduler(object):
    def __init__(self):
        self.ready = Queue() # a Queue of tasks that are ready
        self.taskmap = {} # a dict that keeps track of all active tasks (each task has a unique task id)
        self.exit_waiting = {} # This is a holding area for tasks that are waiting. A dict mapping task ID to tasks waiting for exit
        self.read_waiting = {}
        self.write_waiting = {}

    def waitforread(self, task, fd):
        self.read_waiting[fd] = task

    def waitforwrite(self, task, fd):
        self.write_waiting[fd] = task

    # I/O Polling. Use Select() to determine which file descriptor can be used. Unblock any associated task.
    def iopoll(self, timeout):
        if self.read_waiting or self.write_waiting:
            r,w,e = select.select(self.read_waiting,
                                 self.write_waiting,[], timeout)
            for fd in r: self.schedule(self.read_waiting.pop(fd))
            for fd in w: self.schedule(self.write_waiting.pop(fd))


    def new(self, target): # introduce a new task to the schedule
        newtask = Task(target)
        self.taskmap[newtask.tid] = newtask
        self.schedule(newtask)
        return newtask.tid

    def iotask(self):
        while True:
            if self.ready.empty():
                self.iopoll(None)
            else:
                self.iopoll(0)
            yield

    def schedule(self, task):
        print "schedule task", task.tid
        self.ready.put(task) # put a task onto the ready queue

    def exit(self, task):
        print "Task %d terminated" % task.tid
        del self.taskmap[task.tid]
        # notify other tasks waiting for exit
        # when a task exits, we pop a list of all waiting tasks off out of the waiting area and reschedule them
        for task in self.exit_waiting.pop(task.tid, []):
            self.schedule(task)

    def waitforexit(self, task, waittid):
        if waittid in self.taskmap:
            # makes a task wait for another task. It puts the task in the waiting area.
            self.exit_waiting.setdefault(waittid,[]).append(task)
            return True
        else:
            return False

    def mainloop(self):
        self.new(self.iotask())
        while self.taskmap:
            self.iopoll(0)
            task = self.ready.get()
            try:
                result = task.run()
                if isinstance(result, SystemCall):
                    print "get SystemCall"
                    result.task = task # current task
                    result.sched = self # current Scheduler
                    result.handle()
                    continue
            except StopIteration:
                self.exit(task)
                continue
            self.schedule(task)

#===================================================
#                  echo server
#===================================================
from socket import AF_INET, SOCK_STREAM, socket

def handle_client(client, addr):
    print "Connection from", addr
    while True:
        yield ReadWait(client)
        data = client.recv(65536)
        if not data:
            break
        yield WriteWait(client)
        client.send(data)
    client.close()
    print "client closed"
    yield  # Make the function a generator/coroutine

def server(port):
    print "server starting"
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(("", port))
    sock.listen(5)
    # main server loop. Wait for a connection, launch a new task to handle each client
    while True:
        yield ReadWait(sock)
        client, addr = sock.accept()
        yield NewTask(handle_client(client, addr))

def alive():
    while True:
        print "I'm alive!"
        yield

#=============================================
#     A Polling Task
#=============================================




def foo():
    print "foo started "
    mytid = (yield GetTid())
    # print "get my id", mytid
    for i in range(2):
        print "I'm foo", mytid
        time.sleep(1)
        yield

def bar():
    print "bar started"
    mytid = yield GetTid()
    # print "get my id", mytid
    for i in range(2): 
        print "I'm bar", mytid
        time.sleep(1)
        yield

def sometask():
    t1 = yield NewTask(foo()) # Launch new task
    print "do something"
    yield KillTask(t1) # kill task 

def task_to_wait():
    for i in range(5):
        print "Im foo"
        yield

def main():
    child = yield NewTask(task_to_wait())
    print "Waiting for child"
    yield WaitTask(child)
    print "Child Done"

if __name__ == '__main__':
    #sched = Scheduler()
    #sched.new(foo())
    #sched.new(bar())
    #sched.new(sometask())
    #sched.new(main())
    #sched.mainloop()
    sched = Scheduler()
    sched.new(alive())
    sched.new(server(45000))
    sched.mainloop()
