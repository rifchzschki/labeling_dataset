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

# Contoh penggunaan:
arr = [12, 3, 5, 7, 4, 19, 26]
map_points = {i: arr[i] for i in range(len(arr))}
three_medians = get_three_medians(map_points)
print(three_medians)