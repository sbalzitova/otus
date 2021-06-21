#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import gzip
from os import listdir, path


class LogReader:
    def __init__(self, file_dir='.'):
        self.report_date = None
        self.file_dir = path.join(path.dirname(__file__)[:-3], file_dir)
        self.file = self.find_latest_file()
        self.if_gz = False

    def find_latest_file(self):
        files = [f for f in listdir(self.file_dir)]
        max_date = '11111111'
        max_file_name = ''

        for file_name in files:
            if re.findall(r'\d{8}[.][t+xgz]{2,3}', file_name):
                self.report_date = re.findall(r'\d{8}', file_name)
                if self.report_date and self.report_date[0] > max_date:
                    max_date = self.report_date[0]
                    max_file_name = file_name

        self.report_date = max_date
        return max_file_name

    def read_file(self):
        if '.gz' in self.file:
            self.if_gz = True
            return self._read_line_gzip()

        else:
            return self._read_line_plain()

    def _read_line_gzip(self):
        if self.file:
            for line in gzip.open(self.file, 'r'):
                yield line.strip(b'\n').split(b' ')

    def _read_line_plain(self):
        if self.file:
            for line in open(self.file, 'r'):
                yield line[:-3].split(' ')
