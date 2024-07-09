import math
from shapely.geometry import Polygon

def getBound(coordinates):
    print(coordinates)
    polygon = Polygon(coordinates)
    centroid = polygon.centroid
    # centroid_coords = (centroid.x, centroid.y)
    top_left = None
    top_right = None
    bottom_left = None
    bottom_right = None

    max_dist_tl = -1
    max_dist_tr = -1
    max_dist_bl = -1
    max_dist_br = -1

    for point in coordinates:
        x = point[0]
        y = point[1]
        dist = math.hypot(centroid.x - x, centroid.y - y)

        if x <= centroid.x and y <= centroid.y:
            if dist > max_dist_tl:
                max_dist_tl = dist
                top_left = point
        elif x >= centroid.x and y <= centroid.y:
            if dist > max_dist_tr:
                max_dist_tr = dist
                top_right = point
        elif x <= centroid.x and y >= centroid.y:
            if dist > max_dist_bl:
                max_dist_bl = dist
                bottom_left = point
        elif x >= centroid.x and y >= centroid.y:
            if dist > max_dist_br:
                max_dist_br = dist
                bottom_right = point

    return top_left, top_right, bottom_left, bottom_right
