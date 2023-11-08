import pandas as pd

from ..outpost_data import OutpostData


def is_number(data_type):
    return data_type == int or data_type == float or data_type == np.int64 or data_type == np.float64


def sort_distances_to_scouts(distances: dict):
    return sorted(distances.items())


def is_valid_value(value):
    return value and not pd.isna(value)


def scanning_beyond_scout_range(distance, mile_range):
    return distance > mile_range


def count_scouts_by_variable(outpost: OutpostData, year, mile_range, variable, target_value):

    def scout_data_and_target_value_are_compatible_data_types(scout_value, target_value):
        if is_number(scout_value) and is_number(target_value):
            return True
        else:
            return type(scout_value) == type(target_value)

    sorted_distances = sort_distances_to_scouts(distances=outpost.distances_to_scouts[year])

    count = 0

    for distance, scout_list in sorted_distances:
        if scanning_beyond_scout_range(distance=distance,
                                       mile_range=mile_range):
            return count
        for scout in scout_list:
            variable_value = scout.data[variable]
            if not is_valid_value(scout.data[variable]):
                continue
            if not scout_data_and_target_value_are_compatible_data_types(scout_value=variable_value,
                                                                         target_value=target_value):
                raise Exception(f"Variable value '{variable_value}' and target value '{target_value}' are"
                                f"incompatible.")

            if variable_value == target_value:
                count += 1

    # Reached end of function without exceeding specified mile_range, so return the final count
    return count
