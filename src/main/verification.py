import subprocess, time, argparse

tmp = "../../data/tmp/"

def runCalculate(engine, target, result):
    # Menjalankan program C++ dengan kedua file sebagai argumen
    result = subprocess.run([engine, target, result], capture_output=True, text=True)

    # Menampilkan output dari program C++
    with open(tmp+"hasil.txt", 'w') as file1:
        file1.write(f'Processing ...')
        file1.write("%s\n" % result.stdout)
        file1.write("%s\n" % result.stderr)

def run(engine, target, result):
        print("Verification process...")
        current_time = time.time()
        runCalculate(engine, tmp+target, tmp+result)
        print(f'\n\nProcessing finished in {time.time() - current_time} seconds')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "verification")
    parser.add_argument("target", type=str, help="Target file SLO (True)")
    parser.add_argument("result", type=str, help="Result from OCR (Check)")
    parser.add_argument("engine", type=str, help="File .exe checker")
    args = parser.parse_args()

    run(args.engine, args.target, args.result)



