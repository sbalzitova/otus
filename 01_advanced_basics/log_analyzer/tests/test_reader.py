import unittest
from src.reader import LogReader


class TestReader(unittest.TestCase):

    def test_date(self):
        reader = LogReader('tests/test_data/reader/test_date')
        file = reader.find_latest_file()
        assert file == 'nginx-access-ui.log-20210202.gz'

    def test_empty_dir(self):
        reader = LogReader('tests/test_data/reader')
        file = reader.find_latest_file()
        assert file == ''

    def test_unknown_format(self):
        reader = LogReader('tests/test_data/reader/test_unknown_format')
        file = reader.find_latest_file()
        assert file == ''


if __name__ == '__main__':
    unittest.main()
