from time import time
from threading import RLock


class LeakyBucket(object):
    '''
    Leaky Bucket algorithm (as metric)
    https://en.wikipedia.org/wiki/Leaky_bucket
    '''

    def __init__(self, capacity, out_bandwidth):
        '''
        Constructor
        :param capacity: capacity of bucket (minimum 64KB), bytes
        :param out_bandwidth: max leaking bandwidth, bps
        '''
        self.max_capacity = max(64*1024, capacity)
        self.occupied_capacity = 0
        self.out_bandwidth = out_bandwidth
        self.last_leak_check = time()
        self.leak_budget = 0
        self.lock = RLock()


    def check(self, bytes):
        '''
        Check does incoming packet conform to available bucket capacity or not
        :param bytes: packet size (max 64KB), bytes
        :return: True/False
        '''
        assert bytes <= 64*1024;
        with self.lock:
            if (self.max_capacity - self.occupied_capacity) >= bytes:
                self.occupied_capacity += bytes
                return True
            else:
                return False

    def leak(self, bytes):
        '''
        Check does packet leak conform to occupied bucket capacity and leaking bandwidth or not
        :param bytes: packet size (max 64KB), bytes
        :return: True/False
        '''
        assert bytes <= 64*1024;
        with self.lock:
            now = time()
            leak_tick = now - self.last_leak_check
            self.last_leak_check = now
            self.leak_budget += leak_tick * self.out_bandwidth * 8
            self.leak_budget = min(self.leak_budget, self.out_bandwidth)  # case when no peak loads > out_bandwidth allowed
            if bytes <= min(self.leak_budget, self.occupied_capacity):
                self.occupied_capacity -= bytes
                self.leak_budget -= bytes
                return True
            else:
                return False
