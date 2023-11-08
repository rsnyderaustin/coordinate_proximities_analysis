from ..outpost_data import OutpostData


def now_scanning_outside_of_specified_range(distance, distance_range):
    return distance > distance_range


def num_scouts_in_range(outpost: OutpostData, time_interval, distance_range):
    try:
        distances_to_scouts_dict = outpost.distances_to_scouts[time_interval]
    except KeyError:
        outpost.query_data[time_interval][f"Number of objects in {distance_range} miles"] = None
        return
    sorted_items = sorted(distances_to_scouts_dict.items())
    count = 0
    for distance, scout_list in sorted_items:
        for scout in scout_list:
            if now_scanning_outside_of_specified_range(distance, distance_range):
                return count
            else:
                count += 1
    return count
