from os import path
from src.report_builder import ReportBuilder
import argparse
from json.decoder import JSONDecodeError
import json


parser = argparse.ArgumentParser()
parser.add_argument('--config', type=str, help='Config file for your log report_builder')
args = parser.parse_args()


def parse_config(config_file):
    path_to_config = path.join(path.dirname(__file__), config_file)
    path_to_default_config = path.join(path.dirname(__file__), 'default_config.json')

    def open_config_file(file):
        with open(file, 'r') as d:
            try:
                config_json = json.load(d)
            except JSONDecodeError:
                config_json = {}
        return config_json

    config = open_config_file(path_to_config)
    default_config = open_config_file(path_to_default_config)

    if not config.get('REPORT_SIZE'):
        config['REPORT_SIZE'] = default_config['REPORT_SIZE']

    if not config.get('REPORT_DIR'):
        config['REPORT_DIR'] = default_config['REPORT_DIR']

    if not config.get('LOG_DIR'):
        config['LOG_DIR'] = default_config['LOG_DIR']

    return config


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


def main():
    processed_config = parse_config(args.config)
    report_builder = ReportBuilder(processed_config)

    log_generator = report_builder.read_file()

    is_report_created = path.isfile(path.join(path.dirname(__file__),
                                              report_builder.report_dir,
                                              'report-{}.html'.format(report_builder.reader.report_date)))

    if not is_report_created:
        url_time, parsed_percentage = parse_log(log_generator)

        if parsed_percentage > 80:
            print('{}% of the log cant be processed, check if format changed or file missed'.format(parsed_percentage))

        else:
            for url_time_pair in url_time:
                report_builder.statistics.register_url(*url_time_pair)

        report_builder.form_report()

    else:
        print('Report for {} has already been created, check {}'.format(report_builder.reader.report_date,
                                                                        report_builder.report_dir))


if __name__ == '__main__':
    main()
