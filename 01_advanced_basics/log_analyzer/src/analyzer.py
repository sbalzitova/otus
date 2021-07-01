from .reader import LogReader
from .log import Log
import json
from .monitoring import monitoring
from os import makedirs, path
from collections import OrderedDict
from string import Template
from json.decoder import JSONDecodeError


class LogAnalyzer:
    def __init__(self, config_file):
        self.config_file = config_file
        self.report_size = 1000
        self.report_dir = './reports'
        self.log_dir = './log'
        self.reader = None
        self.log = Log()

    def create_directories(self):
        makedirs(self.report_dir, exist_ok=True)

    def is_report_new(self):
        return path.isdir('{}/report-{}.html'.format(self.report_dir, self.reader.report_date))

    def parse_config(self):

        path_to_config = path.join(path.dirname(__file__)[:-3], self.config_file)
        with open(path_to_config, 'r') as d:
            try:
                config_json = json.load(d)
            except JSONDecodeError:
                config_json = {}

        if config_json.get('REPORT_SIZE'):
            self.report_size = config_json['REPORT_SIZE']

        if config_json.get('REPORT_DIR'):
            self.report_dir = config_json['REPORT_DIR']

        if config_json.get('LOG_DIR'):
            self.log_dir = config_json['LOG_DIR']

    @monitoring
    def parse_log(self):
        is_new = self.is_report_new()

        if is_new:
            log_reader = self.reader.read_file()

            for line in log_reader:
                try:
                    url = line[7]
                    request_time = line[-1]

                except IndexError:
                    url = 'broken url'
                    request_time = 0
                    self.log.error_count += 1

                self.log.register_url(url, request_time)
            non_parsed_log = (self.log.error_count * 100) / self.log.all_count if self.log.all_count else 100

            if non_parsed_log < 80:
                self.log.update_overall_percentages()
                self.form_report()

            else:
                return '{}% of the log cannot be processed, please check if format has changed or file missed'\
                    .format(non_parsed_log)

        else:
            return 'Report for {} has already been created, check {}'.format(self.reader.report_date, self.report_dir)

    @monitoring
    def form_report(self):
        if self.is_report_new and self.log.data:
            report_data = []
            ordered_data = OrderedDict(sorted(self.log.data.items(), key=lambda q: -q[1]['time_sum']))

            for k, v in ordered_data.items():
                v.pop('all_request_times', None)
                report_data.append(v)
                self.report_size -= 1

                if self.report_size == 0:
                    break

            report_file = path.join(self.report_dir, 'report-{}.html'.format(self.reader.report_date))

            with open('report.html', 'r') as source:
                text = source.read()
                template = Template(text)

                with open(report_file, 'w+') as target:
                    target.write(template.safe_substitute(table_json=report_data))

    def start(self):
        self.parse_config()
        self.reader = LogReader(self.log_dir)
        self.create_directories()
        self.parse_log()
        self.form_report()
