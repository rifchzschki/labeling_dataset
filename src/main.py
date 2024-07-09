import time, os
import roboflow as rb
import yolov8 as yv8

# loop all the images in the folder
for os.path in os.listdir('../data/input'):
    print

image_path = '../assets/your_image.jpg'
model_path = '../model/best.pt'
algo = input("Input model:\n1. Roboflow\n2. yolov8\n:")
start_time = time.time()
if(algo=="1"):
    rb.run(image_path)
else:
    yv8.run(image_path)
print(time.time()-start_time)