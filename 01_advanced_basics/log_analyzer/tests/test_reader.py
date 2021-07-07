import unittest
from main import find_latest_file


class TestReader(unittest.TestCase):

    def test_date(self):
        file, date = find_latest_file('tests/test_data/reader/test_date')
        assert file == 'nginx-access-ui.log-20210202.gz'

    def test_empty_dir(self):
        file, date = find_latest_file('tests/test_data/reader')
        assert file is None

    def test_unknown_format(self):
        file, date = find_latest_file('tests/test_data/reader/test_unknown_format')
        assert file is None


if __name__ == '__main__':
    unittest.main()
