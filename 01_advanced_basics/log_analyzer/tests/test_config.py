import unittest
from src.analyzer import LogAnalyzer


class TestLog(unittest.TestCase):
    def test_empty_config(self):
        analyzer = LogAnalyzer('tests/test_data/config/empty_config.json')
        analyzer.parse_config()
        assert analyzer.report_size == 1000 and analyzer.report_dir == './reports' and analyzer.log_dir == './log'

    def test_no_size_in_config(self):
        analyzer = LogAnalyzer('tests/test_data/config/no_size_config.json')
        analyzer.parse_config()
        assert analyzer.report_size == 1000 and analyzer.report_dir == './reports_path' and analyzer.log_dir == './log_path'

    def test_no_log_in_config(self):
        analyzer = LogAnalyzer('tests/test_data/config/no_log_config.json')
        analyzer.parse_config()
        assert analyzer.report_size == 2000 and analyzer.report_dir == './reports_path' and analyzer.log_dir == './log'

    def test_no_report_in_config(self):
        analyzer = LogAnalyzer('tests/test_data/config/no_report_config.json')
        analyzer.parse_config()
        assert analyzer.report_size == 2000 and analyzer.report_dir == './reports' and analyzer.log_dir == './log_path'

    def test_full_config(self):
        analyzer = LogAnalyzer('tests/test_data/config/full_config.json')
        analyzer.parse_config()
        assert analyzer.report_size == 2000 and analyzer.report_dir == './reports_path' and analyzer.log_dir == './log_path'
