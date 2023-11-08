import pandas as pd
from typing import Union

from . import outpost_functions
from .outpost_data import OutpostData


class OutpostsManager:

    def __init__(self):
        # coordinate: Outpost
        self.outposts = {}

    def create_outposts(self, dataframe: pd.DataFrame, lat_column_name: str, lon_column_name: str,
                        extra_column_names: Union[list, None] = None):
        for row_index in dataframe.index:
            latitude = dataframe.loc[row_index, lat_column_name]
            longitude = dataframe.loc[row_index, lon_column_name]
            coordinate = (latitude, longitude)

            new_outpost = OutpostData(coordinate=coordinate)

            for extra_column_name in extra_column_names:
                new_outpost.add_data(variable_name=extra_column_name,
                                     value=dataframe.loc[row_index, extra_column_name])

            self.outposts[coordinate] = new_outpost

    def scout_in_range_tf(self, time_interval, distance_range):
        for outpost in self.outposts.values():
            time_interval_result = outpost_functions.scout_in_range_tf(outpost=outpost,
                                                              time_interval=time_interval,
                                                              distance_range=distance_range
                                                              )
            query_str = f"Scout found within {distance_range} miles"
            outpost.add_query_data(time_interval=time_interval,
                                   query_string=query_str,
                                   value=time_interval_result
                                   )

    def num_scouts_in_range(self, time_interval, distance_range):
        for outpost in self.outposts.values():
            time_interval_result = outpost_functions.num_scouts_in_range(outpost=outpost,
                                                                time_interval=time_interval,
                                                                distance_range=distance_range
                                                                )
            query_str = f"Number of scouts within {distance_range} miles"
            outpost.add_query_data(time_interval=time_interval,
                                   query_string=query_str,
                                   value=time_interval_result
                                   )

    def count_scouts_by_variable(self, time_interval, distance_range, variable, target_value):
        for coordinate, outpost in self.outposts.items():
            time_interval_result = outpost_functions.count_scouts_by_variable(outpost=outpost,
                                                                     time_interval=time_interval,
                                                                     distance_range=distance_range,
                                                                     variable=variable,
                                                                     target_value=target_value
                                                                     )
            query_str = (f"Number of scouts within {distance_range} miles with variable '{variable}' equal to target value "
                         f"'{target_value}'")
            outpost.add_query_data(time_interval=time_interval,
                                   query_string=query_str,
                                   value=time_interval_result)

    def average_scouts_by_variable(self, time_interval, distance_range, variable):
        for coordinate, outpost in self.outposts.items():
            time_interval_result = outpost_functions.average_scouts_by_variable(outpost=outpost,
                                                                       time_interval=time_interval,
                                                                       distance_range=distance_range,
                                                                       variable=variable
                                                                       )
            query_str = f"Average '{variable}' of scouts within {distance_range} miles"
            outpost.add_query_data(time_interval=time_interval,
                                   query_string=query_str,
                                   value=time_interval_result
                                   )

    def nearest_scout(self, time_interval):
        for coordinate, outpost in self.outposts.items():
            time_interval_result = outpost_functions.nearest_scout(outpost=outpost,
                                                          time_interval=time_interval)
            query_str = "Nearest scout"
            outpost.add_query_data(time_interval=time_interval,
                                   query_string=query_str,
                                   value=time_interval_result
                                   )

    def get_output_data(self, time_interval):
        output_data = {}
        for outpost in self.outposts.values():
            output_data.setdefault('latitude', []).append(outpost.coordinate[0])
            output_data.setdefault('longitude', []).append(outpost.coordinate[1])
            for key, value in outpost.data.items():
                output_data.setdefault(key, []).append(value)
            for key, value in outpost.query_data[time_interval].items():
                output_data.setdefault(key, []).append(value)

        index_length = max([len(value_list) for value_list in list(output_data.values())])
        index = [time_interval for _ in range(index_length)]
        df = pd.DataFrame(output_data)
        df.insert(loc=0, column='time_interval', value=index)
        return df
