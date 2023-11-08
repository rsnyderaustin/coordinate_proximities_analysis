from typing import Union

import os
import pandas as pd

from coordinate_proximity_analysis import rtree_analysis
from coordinate_proximity_analysis.outpost_processes import OutpostsManager, ScoutsManager
from . import external_data_processing as edp


class EnvironmentManager:

    def __init__(self,
                 mile_range: int,
                 years,
                 outpost_file_path: str,
                 scout_folder_path: str,
                 outpost_lat_col_name: str,
                 outpost_lon_col_name: str,
                 scout_lat_col_name: str,
                 scout_lon_col_name: str,
                 outpost_extra_col_names: Union[list[str], str, None] = None,
                 scout_extra_col_names: Union[list[str], str, None] = None,
                 outpost_sheet_name=None,
                 scout_sheet_name=None
                 ):

        self.mile_range = mile_range

        self.years = self.ensure_list_of_strings(years)

        self.outpost_file_path = outpost_file_path
        self.outpost_sheet_name = outpost_sheet_name

        if isinstance(outpost_extra_col_names, str):
            outpost_extra_col_names = [outpost_extra_col_names]

        self.outpost_columns = {
            'lat': outpost_lat_col_name,
            'lon': outpost_lon_col_name,
            'extra': outpost_extra_col_names
        }
        self.outpost_column_names = edp.combine_column_names(outpost_lat_col_name, outpost_lon_col_name,
                                                             outpost_extra_col_names)

        self.scout_folder_path = scout_folder_path
        self.scout_sheet_name = scout_sheet_name

        if isinstance(scout_extra_col_names, str):
            scout_extra_col_names = [scout_extra_col_names]

        self.scout_columns = {
            'lat': scout_lat_col_name,
            'lon': scout_lon_col_name,
            'extra': scout_extra_col_names
        }
        self.scout_column_names = edp.combine_column_names(scout_lat_col_name, scout_lon_col_name,
                                                           scout_extra_col_names)

        self.outposts_manager = OutpostsManager()
        self.scouts_manager = ScoutsManager()

        self.process_external_data()

    @staticmethod
    def ensure_list_of_strings(variable):
        if isinstance(variable, list) and all(isinstance(item, str) for item in variable):
            return variable

        if isinstance(variable, int):
            return [str(variable)]
        elif isinstance(variable, str):
            return [variable]
        elif isinstance(variable, range):
            return [str(i) for i in variable]

    def process_external_data(self):
        outpost_dataframe = edp.extract_dataframe_by_columns(file_path=self.outpost_file_path,
                                                             column_names=self.outpost_column_names,
                                                             sheet_name=self.outpost_sheet_name)
        self.outposts_manager.create_outposts(dataframe=outpost_dataframe,
                                              lat_column_name=self.outpost_columns['lat'],
                                              lon_column_name=self.outpost_columns['lon'],
                                              extra_column_names=self.outpost_columns['extra'])

        scout_years_dataframes = edp.extract_year_dataframes(folder_path=self.scout_folder_path,
                                                             years=self.years,
                                                             sheet_name=self.scout_sheet_name)
        self.scouts_manager.create_scouts(dataframes_by_year=scout_years_dataframes,
                                          lat_column_name=self.scout_columns['lat'],
                                          lon_column_name=self.scout_columns['lon'],
                                          extra_column_names=self.scout_columns['extra'])

        self.scan_outpost_range()

    def scout_in_range_tf(self, mile_range):
        for year in self.years:
            self.outposts_manager.scout_in_range_tf(year=year,
                                                    mile_range=mile_range)

    def num_scouts_in_range(self, mile_range):
        for year in self.years:
            self.outposts_manager.num_scouts_in_range(year=year,
                                                      mile_range=mile_range)

    def count_scouts_by_variable(self, mile_range, variable, target_value):
        for year in self.years:
            self.outposts_manager.count_scouts_by_variable(year=year,
                                                           mile_range=mile_range,
                                                           variable=variable,
                                                           target_value=target_value)

    def average_scouts_by_variable(self, mile_range, variable):
        for year in self.years:
            self.outposts_manager.average_scouts_by_variable(year=year,
                                                             mile_range=mile_range,
                                                             variable=variable)

    def nearest_scout(self):
        for year in self.years:
            self.outposts_manager.nearest_scout(year=year)

    # Fills the rtree_analysis with the specific
    def scan_outpost_range(self):
        print(f"Starting to scan year {self.years}")

        for year in self.years:
            rtree_analysis.scan_outposts_range(year=year,
                                               outposts=self.outposts_manager.outposts,
                                               scouts=self.scouts_manager.scouts_by_year[year],
                                               mile_range=self.mile_range)
            print(f"Finished scanning year {year}.")

    def combine_current_dataframes(self):
        df_list = []
        for year in self.years:
            output_df = self.outposts_manager.get_output_data(year)
            df_list.append(output_df)
        return pd.concat(df_list, axis=0, ignore_index=True)

    # Dict should be in class-standard format {coordinate: [Scout]}
    def output_data_to_file(self, file_path):
        file_name = os.path.basename(file_path)
        base, extension = os.path.splitext(file_name)

        combined_df = self.combine_current_dataframes()

        if extension in '.csv':
            combined_df.to_csv(file_path, index=False)
        elif extension in '.xlsx':
            combined_df.to_excel(file_path, index=False)
