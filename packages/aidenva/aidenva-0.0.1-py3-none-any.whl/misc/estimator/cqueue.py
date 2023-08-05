
class cQueue:
    def __init__(self, size=10):
        self.size = size
        self._queue = list()

    def q_size(self):
        return len(self._queue)

    def peek(self):
        if(len(self._queue) == 0):
            return None
        return self._queue[0]

    def enqueue(self, value):
        if(len(self._queue) == self.size):
            del self._queue[-1]

        self._queue.insert(0, value)
        return value

    def dequeue(self):
        if(len(self._queue) == 0):
            return None
        v = self._queue[-1]
        del self._queue[-1]
        return v

    def __str__(self):
        return 'q_size %d' % self.q_size()

    def __unicode__(self):
        return u'q_size %d' % self.q_size()

    def __repr__(self):
        return 'q_size %d' % self.q_size()

if __name__ == '__main__':
    q = cQueue(2)

    print(q.enqueue('1'))
    print(q.enqueue('2'))
    print(q.enqueue('3'))
    print(q.dequeue())
    print('size', q.q_size())
    print(q.peek())
    print(q.dequeue())
    print(q.dequeue())
    print(q.dequeue())
    print('size', q.q_size())

