import math, numpy as np, cv2
from shapely.geometry import Polygon

def crop_image(image, points):
    points = np.array(points, dtype=np.float32)
    
    rect = cv2.boundingRect(points)
    x, y, w, h = rect
    print(rect)
    crop = image[y:y+h, x:x+w].copy()

    # Warping perspective jika diperlukan 
    pts1 = points - points.min(axis=0)
    pts2 = np.float32([[0, 0], [w, 0], [w, h], [0, h]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    result = cv2.warpPerspective(crop, matrix, (w, h))

    return result

def dec_point(p1,p2):
    difference = (p1[0] - p2[0], p1[1] - p2[1])
    return math.sqrt(difference[0]**2 + difference[1]**2)

def get_three_medians(arr):
    sorted_arr = sorted(arr)
    median_index = len(sorted_arr) // 2

    if len(arr) % 2 == 0:
        # Jika panjang array genap, ambil dua elemen di tengah
        median_indices = [median_index - 1, median_index, median_index + 1]
    else:
        # Jika panjang array ganjil, ambil elemen di tengah serta dua elemen tetangganya
        median_indices = [median_index - 1, median_index, median_index + 1]

    # Mengambil tiga median berdasarkan sorted array dan map_points
    return {i: arr[i] for i in median_indices}


def get_horizontal(boxes):
    map_points = {}
    list_length = set()
    max_length_box = [None, None] 
    is_horizontal = []
    max_length = 0
    idx = 0
    for box in boxes:        
        if(len(box)>4):
            idx+=1
            continue
        width = max(dec_point(box[1],box[0]), dec_point(box[2],box[3]))
        height = max(dec_point(box[0],box[3]), dec_point(box[1],box[2]))
        length = max(height, width)
        if(height>width): is_horizontal.append(False)
        else: is_horizontal.append(True)
        if(length > max_length):
            max_length = length
            max_length_box[0] = box
            max_length_box[1] = idx
        map_points[length] = box, is_horizontal[idx]
        list_length.add(length)
        idx+=1
    list_length = list(list_length)
    arr = np.array(list_length)
    sorted_arr = np.sort(arr)
    if(len(list_length)%2==0):
        return [map_points[sorted_arr[(len(sorted_arr)//2)]], map_points[sorted_arr[(len(sorted_arr)//2)+1]]]
    else:
        return [map_points[sorted_arr[(len(sorted_arr)//2)-1]],map_points[sorted_arr[len(sorted_arr)//2]], map_points[sorted_arr[(len(sorted_arr)//2)+1]]]


def getBound(coordinates):
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
