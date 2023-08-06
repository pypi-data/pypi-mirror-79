from random import Random as DefaultRandom
from queue import Queue


class EntropyBuffer(object):
    def __init__(self, buffer_size):
        self.bytes_queue = Queue(maxsize=buffer_size)

    def enqueue(self, b):
        for byte in b:
            self.bytes_queue.put(byte)

    def dequeue(self, k):
        a = [self.bytes_queue.get(block=True) for i in range(k)]
        return b''.join(a)


class BaseRandom(DefaultRandom):
    def __init__(self, buffer_size):
        self.buffer_size = buffer_size
        self.buffer = EntropyBuffer(buffer_size)
        self.gauss_next = None

    def random(self):
        return 1/(2**64/self.getrandbits(64))

    def getrandbits(self, k):
        if k <= 0:
            raise ValueError('number of bits must be greater than zero')
        numbytes = (k + 7) // 8  # bits / 8 and rounded up
        x = int.from_bytes(self.buffer.dequeue(numbytes), 'big')
        return x >> (numbytes * 8 - k)  # trim excess bits

    def _notimplemented(self, *args, **kwds):
        raise NotImplementedError('Randomless entropy source does not have state or seed.')

    getstate = setstate = seed = _notimplemented
