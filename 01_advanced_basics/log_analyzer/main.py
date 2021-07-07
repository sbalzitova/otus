import re
import json
import gzip
import logging
import datetime
import argparse
from string import Template
from os import path, listdir, makedirs
from json.decoder import JSONDecodeError
from src.statistics_builder import StatisticsBuilder


logging.basicConfig(filename='script_log.txt',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%Y.%m.%d %H:%M:%S',
                    level=logging.INFO)

parser = argparse.ArgumentParser()
parser.add_argument('--config', type=str, help='Config file for your log report_builder')
args = parser.parse_args()


def parse_config(config_file):
    path_to_config = path.join(path.dirname(__file__), config_file)

    default_config = {
        "REPORT_SIZE": 1000,
        "REPORT_DIR": "./reports",
        "LOG_DIR": "./log"
    }

    def open_config_file(file):
        with open(file, 'r') as d:
            try:
                config_json = json.load(d)
            except JSONDecodeError:
                return None
        return config_json

    config = open_config_file(path_to_config)
    default_config.update(config)
    return default_config


def find_latest_file(file_dir):
    max_date = None
    max_file_name = None
    report_date = None

    for file_name in listdir(file_dir):
        matched_file = re.match(r'^nginx-access-ui\.log-(?P<date>\d{8})(\.gz)?$', file_name)
        if matched_file:
            report_date = matched_file.groupdict()['date']

            if max_date:
                if report_date and report_date > max_date:
                    max_date = report_date
                    max_file_name = file_name

            else:
                max_date = report_date
                max_file_name = file_name

    if max_date:
        report_date = datetime.datetime.strptime(max_date, '%Y%m%d').date()

    return max_file_name, report_date


def read_file(file, log_dir):
    file_dir = path.join(path.dirname(__file__), log_dir, file)
    file_opener = gzip.open(file_dir, 'r') if file.endswith('.gz') else open(file_dir, 'r')
    for line in file_opener:
        yield line.strip().split()


def parse_log(log_generator):
    error_count = all_count = 0
    url_time_map = []

    for line in log_generator:
        all_count += 1
        try:
            url = line[6]
            request_time = line[-1]

        except IndexError:
            url = 'broken url'
            request_time = 0
            error_count += 1

        url_time_map.append((url, request_time))

    parsed_log_percentage = (error_count * 100) / all_count if all_count else 100

    return url_time_map, parsed_log_percentage


def form_report(statistics, report_date, report_dir, report_size):
    makedirs(report_dir, exist_ok=True)

    if statistics.data:
        ordered_data = sorted(statistics.data.values(), key=lambda i: i['time_avg'], reverse=True)
        report_file = path.join(report_dir, 'report-{}.html'.format(report_date))

        with open('report.html', 'r') as source:
            text = source.read()
            template = Template(text)

            with open(report_file, 'w+') as target:
                target.write(template.safe_substitute(table_json=ordered_data[:report_size]))


def main():
    processed_config = parse_config(args.config)

    if not processed_config:
        logging.error('Config is corrupted')
        return

    log_dir = processed_config.get('LOG_DIR')
    report_size = processed_config.get('REPORT_SIZE')
    report_dir = processed_config.get('REPORT_DIR')

    log_name, log_date = find_latest_file(log_dir)

    statistics = StatisticsBuilder()

    log_generator = read_file(log_name, log_dir)

    is_report_created = path.isfile(path.join(path.dirname(__file__),
                                              report_dir,
                                              'report-{}.html'.format(log_date)))

    if not is_report_created:
        url_time, parsed_percentage = parse_log(log_generator)

        if parsed_percentage > 80:
            logging.error('{}% of the log cant be processed, check if format changed '
                          'or file missed'.format(parsed_percentage))

        else:
            for url_time_pair in url_time:
                statistics.register_url(*url_time_pair)

        form_report(statistics, log_date, report_dir, report_size)
        logging.info('Analysis completed')

    else:
        logging.info('Report for {} has already been created, check {}'.format(log_date, log_dir))


if __name__ == '__main__':
    main()
