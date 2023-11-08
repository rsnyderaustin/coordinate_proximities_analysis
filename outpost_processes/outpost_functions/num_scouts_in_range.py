from ..outpost_data import OutpostData


def now_scanning_outside_of_specified_range(distance, mile_range):
    return distance > mile_range


def num_scouts_in_range(outpost: OutpostData, year, mile_range):
    try:
        distances_to_scouts_dict = outpost.distances_to_scouts[year]
    except KeyError:
        outpost.query_data[year][f"Number of objects in {mile_range} miles"] = None
        return
    sorted_items = sorted(distances_to_scouts_dict.items())
    count = 0
    for distance, scout_list in sorted_items:
        for scout in scout_list:
            if now_scanning_outside_of_specified_range(distance, mile_range):
                return count
            else:
                count += 1
    return count
