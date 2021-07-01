from .monitoring import monitoring


class Log:
    def __init__(self):
        self.data = {}
        self.all_count = 0
        self.all_time = 0
        self.error_count = 0

    @monitoring
    def register_url(self, url, request_time):
        if not self.data.get(url):
            self.data[url] = {
                'count': 0,
                'time_avg': 0,
                'time_max': float('-inf'),
                'time_sum': 0,
                'url': url,
                'time_med': 0,
                'time_perc': 0,
                'count_perc': 0,
                'all_request_times': []
            }

        self.calculations(url, request_time)

    def calculations(self, url, r_t):
        self.data[url]['count'] += 1

        try:
            request_time = float(r_t)

        except ValueError:
            request_time = 0

        self.data[url]['all_request_times'].append(request_time)
        self.data[url]['time_sum'] += request_time
        self.data[url]['time_max'] = self.calc_time_max(url, request_time)
        self.data[url]['time_avg'] = self.calc_time_avg(url)
        self.data[url]['time_med'] = self.calc_time_med(url)

        self.all_count += 1
        self.all_time += request_time

    def calc_time_avg(self, url):
        return self.data[url]['time_sum'] / self.data[url]['count']

    def calc_time_max(self, url, request_time):
        return request_time if request_time > self.data[url]['time_max'] else self.data[url]['time_max']

    def calc_time_med(self, url):
        sorted_arr = sorted(self.data[url]['all_request_times'])
        arr_len = len(sorted_arr)
        return sorted_arr[int(arr_len / 2)]

    def calc_count_percent(self, url):
        url_count = self.data[url]['count']
        percent = (url_count * 100) / self.all_count
        self.data[url]['count_perc'] = percent

    def calc_time_percent(self, url):
        url_time = self.data[url]['time_sum']
        percent = (url_time * 100) / self.all_time
        self.data[url]['time_perc'] = percent

    @monitoring
    def update_overall_percentages(self):
        for url in self.data:
            self.calc_count_percent(url)
            self.calc_time_percent(url)
