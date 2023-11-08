class OutpostData:

    def __init__(self, coordinate: tuple):
        self.coordinate = coordinate

        self.query_data = {}
        self.data = {}

        # year: DistancesToScouts
        self.distances_to_scouts = {}

    def add_data(self, variable_name, value):
        if variable_name in self.data:
            print(f"Overwriting variable name '{variable_name}' value '{self.data[variable_name]}' with new value "
                  f"'{value}'")
        self.data[variable_name] = value

    def add_query_data(self, year, query_string, value):
        if year in self.query_data:
            print(f"Overwriting variable name '{query_string}' value '{self.query_data[year][query_string]}' with new value "
                  f"'{value}'")
        self.query_data.setdefault(year, {})
        self.query_data[year][query_string] = value

    def add_scouts(self, year, scouts, distance):
        self.distances_to_scouts.setdefault(year, {})
        self.distances_to_scouts[year].setdefault(distance, []).extend(scouts)
