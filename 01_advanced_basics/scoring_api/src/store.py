import redis
import logging
import time


class Store:
    def __init__(self, retry=2, expiry=60, host='localhost', port=6379, db=0):
        self.storage = {}
        self.retry = retry
        self.action_count = 0
        self.expiry = expiry
        self.client = redis.Redis(host=host, port=port, db=db)

    # non-redis methods
    def get(self, key):
        return self.storage.get(key)

    def set(self, key, value):
        self.storage[key] = value

    # redis methods
    def cache_get(self, key):
        while self.action_count <= self.retry:
            try:
                return self.client.get(key)
            except Exception as e:
                logging.error(e)
                self.action_count += 1
                time.sleep(3)

    def cache_set(self, key, value, expiry=None):
        while self.action_count <= self.retry:
            try:
                self.client.set(key, value)
                self.client.expire(key, expiry or self.expiry)
                return
            except Exception as e:
                logging.error(e)
                self.action_count += 1
                time.sleep(3)
