import re
import gzip
from os import listdir, path
import datetime


class LogReader:
    def __init__(self, file_dir):
        self.report_date = None
        self.file_dir = path.join(path.dirname(__file__)[:-3], file_dir)
        self.file = path.join(path.dirname(__file__)[:-3], self.file_dir, self.find_latest_file())

    def find_latest_file(self):
        files = [f for f in listdir(self.file_dir)]
        max_date = None
        max_file_name = None

        for file_name in files:
            if re.match(r'^nginx-access-ui\.log-(?P<date>\d{8})(\.gz)?$', file_name):
                self.report_date = re.findall(r'\d{8}', file_name)

                if max_date:
                    if self.report_date and self.report_date[0] > max_date:
                        max_date = self.report_date[0]
                        max_file_name = file_name

                else:
                    max_date = self.report_date[0]
                    max_file_name = file_name

        if max_date:
            self.report_date = datetime.date(int(max_date[:4]), int(max_date[4:6]), int(max_date[6:]))
            return max_file_name
        else:
            return ''

    def read_file(self):
        open_fn = gzip.open(self.file, 'r') if self.file.endswith('.gz') else open(self.file, 'r')

        for line in open_fn:
            yield line.strip().split()
