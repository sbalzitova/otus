import unittest
from src.reader import LogReader


class TestReader(unittest.TestCase):

    def test_date(self):
        reader = LogReader('tests/test_data/reader/test_date')
        assert reader.file == 'nginx-access-ui.log-20210202.gz'

    def test_format_gz(self):
        reader = LogReader('tests/test_data/reader/test_format_gz')
        reader.read_file()
        assert reader.if_gz is True

    def test_format_txt(self):
        reader = LogReader('tests/test_data/reader/test_format_txt')
        reader.read_file()
        assert reader.if_gz is False

    def test_empty_dir(self):
        reader = LogReader('tests/test_data/reader')
        reader.read_file()
        assert reader.file == ''

    def test_unknown_format(self):
        reader = LogReader('tests/test_data/reader/test_unknown_format')
        reader.read_file()
        assert reader.file == ''


if __name__ == '__main__':
    unittest.main()
