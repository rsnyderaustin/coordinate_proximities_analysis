from environment_management.environment_manager import EnvironmentManager

env_manager = EnvironmentManager(time_intervals=2022,
                                 outpost_file_path='',
                                 scout_folder_path='',
                                 outpost_lat_col_name='latitude',
                                 outpost_lon_col_name='longitude',
                                 outpost_extra_col_names='population',
                                 scout_lat_col_name='Site Latitude',
                                 scout_lon_col_name='Site Longitude',
                                 scout_sheet_name='Yearend')
env_manager.count_scouts_by_variable(distance_range=15,
                                     variable='Activity',
                                     target_value='Private Practice')
env_manager.nearest_scout()
env_manager.output_data_to_file(file_path="C:/Users/austisnyder/OrganizedFolder/OutputProgrammingFilesHere/closest_dds.xlsx")

