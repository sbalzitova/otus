import unittest
from main import parse_config


class TestLog(unittest.TestCase):
    def test_empty_config(self):
        conf_file = parse_config('tests/test_data/config/empty_config.json')
        assert conf_file['REPORT_SIZE'] == 1000 and conf_file['REPORT_DIR'] == './reports' and conf_file['LOG_DIR'] == './log'

    def test_no_size_in_config(self):
        conf_file = parse_config('tests/test_data/config/no_size_config.json')
        assert conf_file['REPORT_SIZE'] == 1000 and conf_file['REPORT_DIR'] == './reports_path' and conf_file['LOG_DIR'] == './log_path'

    def test_no_log_in_config(self):
        conf_file = parse_config('tests/test_data/config/no_log_config.json')
        assert conf_file['REPORT_SIZE'] == 2000 and conf_file['REPORT_DIR'] == './reports_path' and conf_file['LOG_DIR'] == './log'

    def test_no_report_in_config(self):
        conf_file = parse_config('tests/test_data/config/no_report_config.json')
        assert conf_file['REPORT_SIZE'] == 2000 and conf_file['REPORT_DIR'] == './reports' and conf_file['LOG_DIR'] == './log_path'

    def test_full_config(self):
        conf_file = parse_config('tests/test_data/config/full_config.json')
        assert conf_file['REPORT_SIZE'] == 2000 and conf_file['REPORT_DIR'] == './reports_path' and conf_file['LOG_DIR'] == './log_path'
