from shapely.geometry import Polygon

def getBound(coordinates):
    polygon = Polygon(coordinates)
    centroid = polygon.centroid
    centroid_coords = (centroid.x, centroid.y)

    x_min, y_min, x_max, y_max = polygon.bounds
    corner_points = [(x_min, y_min), (x_max, y_min), (x_max, y_max), (x_min, y_max)]
    return centroid_coords, corner_points