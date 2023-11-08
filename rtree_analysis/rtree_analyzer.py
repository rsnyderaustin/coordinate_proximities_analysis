from geopy import Point, distance
from rtree import index


def _create_bounding_box(coordinate, distance_range):
    center_point = Point(coordinate[0], coordinate[1])
    north_point = distance.distance(miles=distance_range).destination(center_point, 0)
    south_point = distance.distance(miles=distance_range).destination(center_point, 180)
    east_point = distance.distance(miles=distance_range).destination(center_point, 90)
    west_point = distance.distance(miles=distance_range).destination(center_point, 270)

    left = west_point.longitude
    right = east_point.longitude
    bottom = south_point.latitude
    top = north_point.latitude

    bounding_box = (left, bottom, right, top)
    return bounding_box


def _distance_between(coord1, coord2):
    return distance.geodesic(coord1, coord2).miles


def _get_scout_hubs_in_bounding_box(outpost_coordinate, distance_range, rtree):
    bounding_box = _create_bounding_box(coordinate=outpost_coordinate,
                                        distance_range=distance_range)
    scout_hubs_in_bbox = list(rtree.intersection(bounding_box, objects=True))
    return scout_hubs_in_bbox


def _hub_within_exact_outpost_radius(scout_hub_coordinate, outpost_coordinate, distance_range):
    points_distance = _distance_between(outpost_coordinate, scout_hub_coordinate)
    if points_distance <= distance_range:
        return points_distance
    else:
        return False


def create_rtree(scout_coordinates: list[tuple]):
    rtree = index.Index()
    if not scout_coordinates:
        print("Method create_rtrees called on an empty set of scout coordinates.")

    for i, scout_coordinate_tuple in enumerate(scout_coordinates):
        print(f"Scout coordinate: {scout_coordinate_tuple}")
        latitude, longitude = scout_coordinate_tuple[0], scout_coordinate_tuple[1]
        print(f"Inserting coordinate with lat '{latitude}' and lon '{longitude}' into rtree")
        rtree.insert(i, (longitude, latitude, longitude, latitude))
    return rtree


def scan_outposts_range(time_interval, outposts, scouts, distance_range: int):
    print(f"Creating rtree")
    rtree = create_rtree(scout_coordinates=scouts.keys())
    print(f"Done creating rtree")
    for i, (outpost_coordinate, outpost) in enumerate(outposts.items()):
        scout_hubs_in_bbox = _get_scout_hubs_in_bounding_box(outpost_coordinate, distance_range, rtree)
        if len(scout_hubs_in_bbox) == 0:
            continue

        # Within the bounding box doesn't mean within the circular radius
        for scout_hub in scout_hubs_in_bbox:
            scout_hub_coordinate = (scout_hub.bbox[1], scout_hub.bbox[0])
            distance_result = _hub_within_exact_outpost_radius(scout_hub_coordinate, outpost_coordinate, distance_range)
            if distance_result:
                scouts_in_range = scouts[scout_hub_coordinate]
                outpost.add_scouts(time_interval=time_interval,
                                   scouts=scouts_in_range,
                                   distance=distance_result)
