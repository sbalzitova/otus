import unittest
from src.log import Log


class TestLog(unittest.TestCase):
    log = Log()

    def test_count(self):
        self.log.data = {
            'all': {'all_count': 0, 'all_time': 0},
            'some_url': {
                'url': 'some_url', 'count': 1, 'count_perc': 0, 'time_sum': 3, 'time_perc': 0, 'time_avg': 3.0,
                'time_max': 3, 'time_med': 3, 'all_request_times': [3]
            }
        }
        url = 'some_url'
        request_time = 2
        self.log.register_url(url, request_time)
        assert self.log.data['some_url']['count'] == 2

    def test_time_avg_same_url(self):
        self.log.data = {
            'all': {'all_count': 0, 'all_time': 0},
            'some_url': {
                'url': 'some_url', 'count': 1, 'count_perc': 0, 'time_sum': 3, 'time_perc': 0, 'time_avg': 3.0,
                'time_max': 3, 'time_med': 3, 'all_request_times': [3]
            }
        }
        url = 'some_url'
        request_time = 2
        self.log.register_url(url, request_time)
        assert self.log.data['some_url']['time_avg'] == 2.5

    def test_time_avg_another_url(self):
        self.log.data = {
            'all': {'all_count': 0, 'all_time': 0},
            'some_url': {
                'url': 'some_url', 'count': 1, 'count_perc': 0, 'time_sum': 3, 'time_perc': 0, 'time_avg': 3.0,
                'time_max': 3, 'time_med': 3, 'all_request_times': [3]
            }
        }
        url = 'another_url'
        request_time = 2
        self.log.register_url(url, request_time)
        assert self.log.data['another_url']['time_avg'] == 2.0

    def test_time_sum_same_url(self):
        self.log.data = {
            'all': {'all_count': 0, 'all_time': 0},
            'some_url': {
                'url': 'some_url', 'count': 1, 'count_perc': 0, 'time_sum': 3, 'time_perc': 0, 'time_avg': 3.0,
                'time_max': 3, 'time_med': 3, 'all_request_times': [3]
            }
        }
        url = 'some_url'
        request_time = 2
        self.log.register_url(url, request_time)
        assert self.log.data['some_url']['time_sum'] == 5

    def test_time_sum_another_url(self):
        self.log.data = {
            'all': {'all_count': 0, 'all_time': 0},
            'some_url': {
                'url': 'some_url', 'count': 1, 'count_perc': 0, 'time_sum': 3, 'time_perc': 0, 'time_avg': 3.0,
                'time_max': 3, 'time_med': 3, 'all_request_times': [3]
            }
        }
        url = 'another_url'
        request_time = 2
        self.log.register_url(url, request_time)
        assert self.log.data['some_url']['time_sum'] == 3 and self.log.data['another_url']['time_sum'] == 2

    def test_time_max_same_url(self):
        self.log.data = {
            'all': {'all_count': 0, 'all_time': 0},
            'some_url': {
                'url': 'some_url', 'count': 1, 'count_perc': 0, 'time_sum': 3, 'time_perc': 0, 'time_avg': 3.0,
                'time_max': 3, 'time_med': 3, 'all_request_times': [3]
            }
        }
        url = 'some_url'
        request_time = 6
        self.log.register_url(url, request_time)
        assert self.log.data['some_url']['time_max'] == 6

    def test_time_max_another_url(self):
        self.log.data = {
            'all': {'all_count': 0, 'all_time': 0},
            'some_url': {
                'url': 'some_url', 'count': 1, 'count_perc': 0, 'time_sum': 3, 'time_perc': 0, 'time_avg': 3.0,
                'time_max': 3, 'time_med': 3, 'all_request_times': [3]
            }
        }
        url = 'another_url'
        request_time = 2
        self.log.register_url(url, request_time)
        assert self.log.data['some_url']['time_max'] == 3 and self.log.data['another_url']['time_max'] == 2

    def test_time_med_same_url(self):
        self.log.data = {
            'all': {'all_count': 0, 'all_time': 0},
            'some_url': {
                'url': 'some_url', 'count': 1, 'count_perc': 0, 'time_sum': 3, 'time_perc': 0, 'time_avg': 3.0,
                'time_max': 3, 'time_med': 3, 'all_request_times': [1, 3, 4, 5]
            }
        }
        url = 'some_url'
        request_time = 8
        self.log.register_url(url, request_time)
        assert self.log.data['some_url']['time_med'] == 4

    def test_time_med_another_url(self):
        self.log.data = {
            'all': {'all_count': 0, 'all_time': 0},
            'some_url': {
                'url': 'some_url', 'count': 1, 'count_perc': 0, 'time_sum': 3, 'time_perc': 0, 'time_avg': 3.0,
                'time_max': 3, 'time_med': 3.5, 'all_request_times': [1, 3, 4, 5]
            }
        }
        url = 'another_url'
        request_time = 2
        self.log.register_url(url, request_time)
        assert self.log.data['some_url']['time_med'] == 3.5 and self.log.data['another_url']['time_med'] == 2

    def test_count_perc(self):
        self.log.data = {
            'some_url': {
                'url': 'some_url', 'count': 4, 'count_perc': 0, 'time_sum': 13, 'time_perc': 0, 'time_avg': 3.25,
                'time_max': 5, 'time_med': 3.5, 'all_request_times': [1, 3, 4, 5]
            },
            'another_url': {
                'url': 'another_url', 'count': 3, 'count_perc': 0, 'time_sum': 8, 'time_perc': 0,
                'time_avg': 2.6666666666666665, 'time_max': 4, 'time_med': 3, 'all_request_times': [1, 3, 4]
            }
        }
        self.log.all_count = 7
        self.log.all_time = 21
        self.log.update_overall_percentages()

        rounded_count_perc_some_url = round(self.log.data['some_url']['count_perc'], 3)
        rounded_count_perc_another_url = round(self.log.data['another_url']['count_perc'], 3)

        assert rounded_count_perc_some_url == 57.143 and rounded_count_perc_another_url == 42.857

    def test_time_perc(self):
        self.log.data = {
            'some_url': {
                'url': 'some_url', 'count': 4, 'count_perc': 0, 'time_sum': 13, 'time_perc': 0, 'time_avg': 3.25,
                'time_max': 5, 'time_med': 3.5, 'all_request_times': [1, 3, 4, 5]
            },
            'another_url': {
                'url': 'another_url', 'count': 3, 'count_perc': 0, 'time_sum': 8, 'time_perc': 0,
                'time_avg': 2.6666666666666665, 'time_max': 4, 'time_med': 3, 'all_request_times': [1, 3, 4]
            }
        }
        self.log.all_count = 7
        self.log.all_time = 21

        self.log.update_overall_percentages()

        rounded_time_perc_some_url = round(self.log.data['some_url']['time_perc'], 3)
        rounded_time_perc_another_url = round(self.log.data['another_url']['time_perc'], 3)

        assert rounded_time_perc_some_url == 61.905 and rounded_time_perc_another_url == 38.095


if __name__ == '__main__':
    unittest.main()
