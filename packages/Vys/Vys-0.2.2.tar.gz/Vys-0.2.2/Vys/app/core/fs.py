#! python3
import json
import os
import csv


class Csv:
    def __init__(self, input_file):
        self._input_file = input_file
        self._exec()
        self._count = -1

    def _exec(self):
        self._json_data = []
        with open(self._input_file, newline='') as csvfile:
            reader = csv.reader(csvfile)
            headers = next(reader)
            for c, i in enumerate(reader):
                temp = {}
                for count, item in enumerate(i):
                    temp[headers[count]] = item
                self._json_data.append(temp)

    def __next__(self):
        if self._count < self._json_data.__len__() - 1:
            self._count += 1
            return self._json_data[self._count]
        raise StopIteration()

    def __iter__(self):
        return self

    def __str__(self):
        return str(self._json_data)

    def __getitem__(self, item):
        return self._json_data[item]
