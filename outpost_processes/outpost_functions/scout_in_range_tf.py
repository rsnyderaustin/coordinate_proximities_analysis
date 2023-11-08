from ..outpost_data import OutpostData


def sort_distances_to_scouts(distances: dict):
    return sorted(distances.items())


def scout_in_range_tf(outpost: OutpostData, time_interval, distance_range):
    try:
        sorted_distances = sort_distances_to_scouts(distances=outpost.distances_to_scouts[time_interval])
    except KeyError:
        return None

    closest_scout_hub = sorted_distances[0]
    closest_scout_hub_distance = closest_scout_hub[0]
    return closest_scout_hub_distance <= distance_range
