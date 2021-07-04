from .reader import LogReader
from .statistics_builder import StatisticsBuilder
from os import makedirs, path
from string import Template


class ReportBuilder:
    def __init__(self, config_file):
        self.report_size = config_file['REPORT_SIZE']
        self.report_dir = config_file['REPORT_DIR']
        self.log_dir = config_file['LOG_DIR']
        self.reader = None
        self.statistics = StatisticsBuilder()

    def form_report(self):
        makedirs(self.report_dir, exist_ok=True)

        if self.statistics.data:
            ordered_data = sorted(self.statistics.data.values(), key=lambda i: i['time_avg'], reverse=True)
            report_file = path.join(self.report_dir, 'report-{}.html'.format(self.reader.report_date))

            with open('report.html', 'r') as source:
                text = source.read()
                template = Template(text)

                with open(report_file, 'w+') as target:
                    target.write(template.safe_substitute(table_json=ordered_data[:self.report_size]))

    def read_file(self):
        self.reader = LogReader(self.log_dir)
        return self.reader.read_file()

    def register_url(self, url, time):
        self.statistics.register_url(url, time)
