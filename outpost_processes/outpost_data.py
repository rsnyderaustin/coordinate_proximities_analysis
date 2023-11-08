class OutpostData:

    def __init__(self, coordinate: tuple):
        self.coordinate = coordinate

        self.query_data = {}
        self.data = {}

        # time_interval: DistancesToScouts
        self.distances_to_scouts = {}

    def add_data(self, variable_name, value):
        if variable_name in self.data:
            print(f"Overwriting variable name '{variable_name}' value '{self.data[variable_name]}' with new value "
                  f"'{value}'")
        self.data[variable_name] = value

    def add_query_data(self, time_interval, query_string, value):
        if time_interval in self.query_data:
            print(f"Overwriting variable name '{query_string}' value '{self.query_data[time_interval][query_string]}' with new value "
                  f"'{value}'")
        self.query_data.setdefault(time_interval, {})
        self.query_data[time_interval][query_string] = value

    def add_scouts(self, time_interval, scouts, distance):
        self.distances_to_scouts.setdefault(time_interval, {})
        self.distances_to_scouts[time_interval].setdefault(distance, []).extend(scouts)
