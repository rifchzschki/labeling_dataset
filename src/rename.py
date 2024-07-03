import os

def rename_images_in_folder(folder_path):
    files = os.listdir(folder_path)
    image_files = [f for f in files if f.lower().endswith(('.jpg'))]
    for idx, file_name in enumerate(image_files):
        file_extension = os.path.splitext(file_name)[1]
        new_name = f"{folder_path}_{idx + 1}{file_extension}"
        src = os.path.join(folder_path, file_name)
        dst = os.path.join(folder_path, new_name)
        os.rename(src, dst)
        print(f"Renamed {src} to {dst}")

folders = [
    'test',
    'train',
    'val'
]

for folder in folders:
    rename_images_in_folder(folder)
