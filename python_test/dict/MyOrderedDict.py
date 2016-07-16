#!/usr/bin/env python

class MyOrderedDict(dict):
    # link  [PRE,NEXT,KEY]
    
    def __init__(self, **kwargs):
        super(self.__class__, self).__init__(kwargs)
        self.count = 0
        # self.head = [None, None, None]
        self.link = []
        print kwargs
        for k,v in kwargs.items():
            self.link.append(k)
            self.count += 1
        print "this is ordereddict init"

    def __repr__(self):
        res = ''
        for key in self.link:
            res = res + str((key,self[key])) + '\n'
        return '<ordered dict> \n' + res
       
    __str__ = __repr__ 

    def __setitem__(self, key, value):
        print "this is new set item"
        if key not in self:
            self.link.append(key)
            self.count += 1
        super(self.__class__, self).__setitem__(key,value)

    def __getitem__(self, key):
        if key not in self:
            raise TypeError("there is not key '%s' in this ordereddict" % key)
        return super(self.__class__, self).__getitem__(key)

    def get_by_index(self, index):
        return self[self.link[index]]

if __name__ == '__main__':
    od = MyOrderedDict()
    s = 'abcdefghijklmnopqrstuvwxyz'
    n = range(26)
    tup = zip(s,n)
    for t in tup:
        od[t[0]] = t[1]

    print od
    print [od.get_by_index(x) for x in n]
    print [od[x] for x in s]

