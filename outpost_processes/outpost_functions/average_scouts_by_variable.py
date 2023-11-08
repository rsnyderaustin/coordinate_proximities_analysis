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


def determine_measure_avg(count, total_sum):
    if count == 0:
        return 0
    return float(total_sum) / count


def average_scouts_by_variable(outpost: OutpostData, year, mile_range, variable):

    sorted_distances = sort_distances_to_scouts(distances=outpost.distances_to_scouts[year])

    count = 0
    total_sum = 0

    for distance, scouts_at_same_distance in sorted_distances:
        if scanning_beyond_scout_range(distance=distance,
                                       mile_range=mile_range):
            return determine_measure_avg(count=count,
                                         total_sum=total_sum)
        for scout in scouts_at_same_distance:
            variable_value = scout.data[variable]
            if not is_valid_value(variable_value):
                continue
            if not is_number(variable_value):
                raise Exception(f"Variable value '{variable_value}' is not expected type int or float for average "
                                f"function.")

            total_sum += variable_value
            count += 1

    # Reached end of function without exceeding specified mile_range, so fill outpost_processes value with final result
    return determine_measure_avg(count=count,
                                 total_sum=total_sum)
