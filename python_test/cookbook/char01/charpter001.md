##

1. \* 表达式用来分解可迭代对象(python2中不支持)

		lst = [1,2,3,4,5]
		head , *tail = lst

2. ' _ '  丢弃不需要的值
3. 对最后几项做有限历史记录可用deque
4. 寻找某个集合最大的n个元素,可用heapq 最大堆

		heapq.nlargest(n, list)

5. 优先队列可用一个三元组 (-priority, index, item )来实现


