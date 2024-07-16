import subprocess
import time
import os
import cv2
import paddleExec

# Nama file executable
executable = './evaluate'

# Nama file input
folder_after = '../data/output/'
folder_before = '../data/input/'
input_file1 = 'SLOText.txt'
input_file2 = 'SebelumPaddle.txt'
output = 'hasil.txt'

def runCalculate(path):
    # Menjalankan program C++ dengan kedua file sebagai argumen
    result = subprocess.run([executable, input_file1, input_file2], capture_output=True, text=True)

    # Menampilkan output dari program C++
    with open(output, 'a') as file1:
        file1.write(f'Processing {path}...')
        file1.write("%s\n" % result.stdout)
        file1.write("%s\n" % result.stderr)

def run():
        current_time = time.time()
        for image_path in os.listdir(folder_after):
            print(f'Processing {image_path}...')
            image_path = os.path.join(folder_after, image_path)
            paddleExec.run(image_path, input_file2)
            runCalculate(image_path)

        print(f'\n\nProcessing finished in {time.time() - current_time} seconds')

run()