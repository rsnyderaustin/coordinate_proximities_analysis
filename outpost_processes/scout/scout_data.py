from typing import Union


class ScoutData:

    def __init__(self, coordinate: tuple, data: Union[dict, None] = None):
        self.data = data or {}

        self.coordinate = coordinate

    def add_data(self, variable_name, value):
        self.data[variable_name] = value
