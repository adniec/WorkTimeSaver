from datetime import timedelta
import re
from salary import *


class Record:
    def __init__(self, date, end_time):
        self.date = date.strftime('%d.%m')
        self.start = timedelta(hours=date.hour, minutes=date.minute)
        self.end = timedelta(hours=end_time.hour, minutes=end_time.minute)

    def __repr__(self):
        return f'<Work day {self.date} from {self.get_hour(self.start)} to {self.get_hour(self.end)} hour>'

    def __str__(self):
        return f'{self.date}\t\t{self.get_hour(self.start)}-{self.get_hour(self.end)}\t' \
            f'{self.get_hour(self.end - self.start)}h'

    def get_hour(self, hour):
        return f'{hour.seconds // 3600:02}:{hour.seconds // 60 % 60:02}'


class Document:
    def __init__(self, date, end_time):
        self.document = str(date.year) + '.txt'
        self.month = date.month
        self.record = Record(date, end_time)
        self.salary = Salary()

    def __repr__(self):
        return f'<Document "{self.document}" with new record {self.record.__repr__()}>'

    def process_file(self):
        lines = self.get_lines()
        if lines:
            self.sum_month(lines)
            month = self.get_month(list(self.get_lines())[0])
            if month != self.month:
                self.save_data(self.salary)
                self.salary = Salary()
        self.save_data(self.record)
        self.sum_month([str(self.record)])
        return f'{sum(self.salary.calculate_salary()):.2f}{self.salary.get_currency()}'

    def sum_month(self, lines):
        for line in lines:
            time = self.get_minutes(line)
            if not time:
                break
            self.salary.update_work(time)

    def get_info(self, pattern, line):
        try:
            return re.search(pattern, line).group(1)
        except AttributeError:
            return False

    def get_minutes(self, line):
        result = self.get_info("\t(..:..)h", line)
        if result:
            time = result.split(":")
            return int(time[0]) * 60 + int(time[1])
        return False

    def get_month(self, line):
        result = self.get_info(".(..)\t", line)
        if result:
            return int(result)
        return 0

    def get_lines(self):
        try:
            with open(self.document, 'r') as f:
                return reversed(f.readlines())
        except FileNotFoundError:
            return False

    def save_data(self, data):
        with open(self.document, 'a+') as f:
            print(data, file=f)
