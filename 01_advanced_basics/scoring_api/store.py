import redis
import logging


class Store:
    def __init__(self, retry=10, expiry=60):
        self.storage = {}
        self.retry = retry
        self.expiry = expiry
        self.client = redis.Redis(host='localhost', port=6379, db=0)

    def get(self, key):
        return self.client.get(key)

    def cache_get(self, key):
        return self.client.get(key)

    def set(self, key, value, expiry):
        self.client.set(key, value)
        self.client.expire(key, expiry)

    def cache_set(self, key, value, expiry):
        self.client.set(key, value)
        self.client.expire(key, expiry)
