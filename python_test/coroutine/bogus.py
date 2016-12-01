#!/usr/bin/python

def printer(n):
    print "printer", n
    return n

def countDown(n):
    print "Counting down from", n
    while n >= 0:
        newvalue = (yield printer(n))
        print "newvalue:", newvalue
        # If a new value got sent in, reset n with it 
        if newvalue is not None:
            n = newvalue
        else:
            n -= 1

if __name__ == '__main__':
    c = countDown(5)
    for n  in c:
        print n 
        if n == 4:
            c.send(2)
