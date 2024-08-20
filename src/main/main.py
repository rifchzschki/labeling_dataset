import argparse, subprocess, time, os

dir_tmp = '../../data/tmp/'

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Menjalankan dua program secara sekuensial.")
    parser.add_argument("--image_name", type=str, required=True, help="Image name")
    parser.add_argument("--invers", type=str, required=True, help="True means prep->seg")
    parser.add_argument("--output", type=str, required=True, help="Output file")
    parser.add_argument("--target", type=str, required=True, help="Target file SLO (True)")
    parser.add_argument("--engine", type=str, required=True, help="File .exe checker")
    parser.add_argument("--prep", type=str, required=True, help="Step")
    parser.add_argument("--ocr", type=str, required=True, help="Step")
    parser.add_argument("--verif", type=str, required=True, help="Step")
    args = parser.parse_args()

    curr_time = time.time()
    if(args.prep == "y"):
        try:
            print("Menjalankan Pre-OCR...")
            current_time = time.time()
            subprocess.run(["../../.venv/Scripts/python", "Pre-OCR.py", str(os.path.basename(args.image_name)), str(args.image_name), str(args.invers)], check=True)
            print(f"Duration: {time.time()-current_time}")
            print("Pre-OCR selesai.")
        except subprocess.CalledProcessError as e:
            print(f"Error menjalankan Pre-OCR: {e}")
    
    if(args.ocr == "y"):
        try:
            print("Menjalankan OCR engine...")
            current_time = time.time()
            subprocess.run(["../../.venv/Scripts/python", "engine.py", dir_tmp+str(args.image_name), dir_tmp+str(args.output)], check=True)
            print(f"Duration: {time.time()-current_time}")
            print("OCR engine selesai.")
        except subprocess.CalledProcessError as e:
            print(f"Error menjalankan engine.py: {e}")

    if(args.verif == "y"):    
        try:
            print("Menjalankan verifikasi...")
            current_time = time.time()
            subprocess.run(["../../.venv/Scripts/python", "verification.py", str(args.target), str(args.output), str(args.engine)], check=True)
            print(f"Duration: {time.time()-current_time}")
            print("OCR engine selesai.")
        except subprocess.CalledProcessError as e:
            print(f"Error menjalankan engine.py: {e}")

    print(f"Total of all step is {time.time()-curr_time}")

