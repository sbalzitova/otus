#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .reader import LogReader
from .log import Log
import json
from .monitoring import monitoring
from os import listdir, makedirs, replace, rename
from collections import OrderedDict
import datetime


class LogAnalyzer:
    def __init__(self, config_file='./default_config.json'):
        self.config_file = config_file
        self.report_size = None
        self.report_dir = None
        self.log_dir = None
        self.is_report_new = True
        self.reader = LogReader()
        self.log = Log()

        self._parse_config()
        self._create_directories()
        self._is_report_new()

    def _create_directories(self):
        makedirs(self.report_dir, exist_ok=True)
        makedirs(self.log_dir, exist_ok=True)

    def _is_report_new(self):
        for f in listdir(self.report_dir):
            if self.reader.report_date in f:
                self.is_report_new = False

    def _parse_config(self):
        with open(self.config_file, 'r') as d:
            d = json.load(d)
            config_json = d

        if config_json.get('REPORT_SIZE'):
            self.report_size = config_json['REPORT_SIZE']

        if config_json.get('REPORT_DIR'):
            self.report_dir = config_json['REPORT_DIR']

        if config_json.get('LOG_DIR'):
            self.log_dir = config_json['LOG_DIR']

    @monitoring
    def parse_log(self):

        if self.is_report_new:
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
                self._form_report()

            else:
                return '{}% of the log cannot be processed, please check if format has changed or file missed'\
                    .format(non_parsed_log)

        else:
            return 'Report for {} has already been created, check {}'.format(self.reader.report_date, self.report_dir)

    @monitoring
    def _form_report(self):
        if self.is_report_new and self.log.data:
            report_data = []
            ordered_data = OrderedDict(sorted(self.log.data.items(), key=lambda q: -q[1]['time_sum']))

            for k, v in ordered_data.items():
                v.pop('all_request_times', None)
                report_data.append(v)
                self.report_size -= 1

                if self.report_size == 0:
                    break

            report_file = self.report_dir + '/report-{}.html'.format(self.reader.report_date)

            with open(report_file, 'w') as target:
                with open('report.html', 'r') as source:

                    for line in source:
                        if '$table_json' in line:
                            target.write('    var table = {};'.format(report_data))
                        else:
                            target.write(line)

    def move_monitoring_log(self):
        replace('monitoring.txt', self.log_dir + '/monitoring-{}.txt'.format(datetime.datetime.now()))

    def start(self):
        self.parse_log()
        self.move_monitoring_log()
