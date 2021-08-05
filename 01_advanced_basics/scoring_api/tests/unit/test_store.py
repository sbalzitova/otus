import unittest
import time

from src.store import Store


class TestStore(unittest.TestCase):

    def test_cache_get(self):
        store = Store(retry=0, expiry=20)
        store.cache_set('bonnie', 'clyde')
        value = store.cache_get('bonnie')
        self.assertEqual(value, b'clyde')

    def test_timeout_default_expiry(self):
        store = Store(retry=0, expiry=1)
        store.cache_set('beauty', 'beast')
        time.sleep(2)
        value = store.cache_get('beauty')
        self.assertEqual(value, None)

    def test_timeout_override_expiry(self):
        store = Store(retry=0, expiry=20)
        store.cache_set('lelik', 'bolik', 1)
        time.sleep(2)
        value = store.cache_get('lelik')
        self.assertEqual(value, None)

    def test_get(self):
        store = Store(retry=0, expiry=20)
        store.set('sid', 'nancy')
        value = store.get('sid')
        self.assertEqual(value, 'nancy')

    def test_get_retry(self):
        store = Store(host='non_existent', retry=1, expiry=20)
        store.cache_set('sid', 'nancy')
        store.cache_get('sid')
        self.assertEqual(store.action_count, 2)

    def test_set_retry(self):
        store = Store(host='non_existent', retry=1, expiry=20)
        store.cache_set('sid', 'nancy')
        self.assertEqual(store.action_count, 2)
