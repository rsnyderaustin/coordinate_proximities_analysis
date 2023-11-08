from environment_management.environment_manager import EnvironmentManager

env_manager = EnvironmentManager(mile_range=20,
                                 years=2022,
                                 outpost_file_path="C:/Users/austisnyder/OrganizedFolder/OutputProgrammingFilesHere/county_sub_pops.csv",
                                 scout_folder_path="K:/DOCUMENT/DENTAL/Year_end_data/Yearend_2022/DDS Primary Input",
                                 outpost_lat_col_name='lat',
                                 outpost_lon_col_name='lon',
                                 outpost_extra_col_names='population',
                                 scout_lat_col_name='Site Latitude',
                                 scout_lon_col_name='Site Longitude',
                                 scout_sheet_name='Yearend')
env_manager.nearest_scout()
env_manager.output_data_to_file(file_path="C:/Users/austisnyder/OrganizedFolder/OutputProgrammingFilesHere/closest_dds.xlsx")

