from coordinate_proximity_analysis.outpost_processes.scout.scout_data import ScoutData
import pandas as pd


class ScoutsManager:

    def __init__(self):
        # year: { coordinate: Scout }
        self.scouts_by_year = {}

    def create_scouts(self, dataframes_by_year: dict, lat_column_name: str, lon_column_name: str,
                      extra_column_names: list):

        def get_coordinate(df, latitude_column_name, longitude_column_name):
            latitude = df.loc[row_index, latitude_column_name]
            longitude = df.loc[row_index, longitude_column_name]
            coordinate = (latitude, longitude)
            return coordinate

        for year, df in dataframes_by_year.items():
            coordinates = []
            self.scouts_by_year.setdefault(year, {})
            for row_index in df.index:
                coordinate = get_coordinate(df, lat_column_name, lon_column_name)
                coordinates.append(coordinate)
                new_scout = ScoutData(coordinate=coordinate)
                self.scouts_by_year[year].setdefault(coordinate, []).append(new_scout)

                if not extra_column_names:
                    continue

                for i, col_name in enumerate(extra_column_names):
                    value = df.loc[row_index, col_name]
                    new_scout.add_data(variable_name=col_name, value=value)
