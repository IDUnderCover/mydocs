#!/usr/bin/python2

class A(object):

    def __init__(self):
        self.a = 1
        self.b = 1

    def __iter__(self):
        print "call __iter__"
        return self

    def next(self):
        print 'call __next__'
        self.a, self.b = self.b, self.a + self.b
        if self.a > 10000:
            raise StopIteration()
        return self.a + self.b


class Chain(object):

    def __init__(self, path=None):
        self.path = path or ""

    def __getattr__(self, item):
        return self.__class__("%s/%s" % (self.path, item))

    def __str__(self):
        return self.path

    __repr__ = __str__
if __name__ == '__main__':
    a = A()
    b = iter(a)
    print b

    print Chain().status.name.pip.start

    # for i in a:
    #     print 'this is form i ' + str(i)
    #     print a.next()