#! python3
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time

import sys


class DatetimeGenerator:
    def __init__(
            self,
            output_format='datetime',
            str_format=None,
            input_value=None,
            input_format=None,
            output_str_format=None
    ):
        self.output_format = output_format
        self.str_format = str_format
        self.input_format = input_format if input_value else 'datetime'
        self.output_str_format = output_str_format
        self._construct = input_value or datetime.today()
        self._formats = ['unix', 'iso', 'datetime', 'string']
        self._exec()

    @property
    def datetime(self):
        return self._construct

    @property
    def iso(self):
        return self._construct.isoformat()

    @property
    def unix(self):
        return time.mktime(self._construct.timetuple())

    @property
    def string(self):
        return datetime.strftime(self._construct, self.output_str_format)

    @property
    def input_datetime(self):
        return self._construct

    @property
    def input_iso(self):
        return self._construct.isoformat()

    @property
    def input_unix(self):
        return datetime.fromtimestamp(self._construct)

    @property
    def input_string(self):
        return datetime.strptime(self._construct, self.str_format)

    def add(self, **kwargs):
        for k, v in kwargs.items():
            self._construct += getattr(sys.modules[__name__], k)(v)

    def subtract(self, **kwargs):
        for k, v in kwargs.items():
            self._construct -= getattr(sys.modules[__name__], k)(v)

    def _exec(self):
        if self.input_format not in self._formats:
            raise Exception(f'Invalid date format - {self.input_format}')
        self._construct = getattr(self, f'input_{self.input_format}')

    def __str__(self):
        return str(getattr(self, self.output_format))

    def __add__(self, other):
        self._construct += other
        return self._construct + other

    def __sub__(self, other):
        self._construct -= other
        return self._construct - other


def hour(hours):
    return timedelta(hours=hours)


def minute(minutes):
    return timedelta(minutes=minutes)


def second(seconds):
    return timedelta(seconds=seconds)


def day(days):
    return timedelta(days=days)


def month(months):
    return relativedelta(months=months)


def year(years):
    return relativedelta(years=years)


class DatetimeConstruct:
    def __init__(self, **kwargs):
        self.date_obj = timedelta()
        for date_format in kwargs:
            self.date_obj += getattr(self, date_format)(kwargs[date_format])

    @staticmethod
    def hour(hours):
        return timedelta(hours=hours)

    @staticmethod
    def minute(minutes):
        return timedelta(minutes=minutes)

    @staticmethod
    def second(seconds):
        return timedelta(seconds=seconds)

    @staticmethod
    def day(days):
        return timedelta(days=days)

    @staticmethod
    def month(months):
        return relativedelta(months=months)

    @staticmethod
    def year(years):
        return relativedelta(years=years)

    def __add__(self, other):
        return self.date_obj + other

    def __sub__(self, other):
        return self.date_obj - other

    def __str__(self):
        return str(self.date_obj)

    def __int__(self):
        return self.date_obj


if __name__ == '__main__':
    p = DatetimeGenerator()
    x = p
    print(p)
    x.add(day=28)
    print(p)
    print(x)

    # p = DatetimeGenerator(input_format='unix', input_value=1599934193, output_format='iso')
    # print(p)
    # p.add(hour=8)
    # print(p)
    # p + hour(1)
    # print(p)
    # f = timedelta(days=9, hours=9)
    # f = DatetimeConstruct(hour=8, day=12)
    # p + f.date_obj
    # print(p)
    # g = timedelta(hours=1)
    # print(f + g)
    # print(f)
    # p + f.date_obj
    # print(p)

    # print(f + p)
    # k = f + p
    # print(k)
