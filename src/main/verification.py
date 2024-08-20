import subprocess, time, argparse
from evaluate import calculate_matrix

tmp = "../../data/tmp/"

def runCalculate( target, result):
    # Menjalankan program C++ dengan kedua file sebagai argumen
    result = calculate_matrix(target, result)

    # Menampilkan output dari program C++
    with open(tmp+"hasil.txt", 'w') as file1:
        file1.write(f'Processing ...')
        file1.write(result)

def run(target, result):
        print("Verification process...")
        current_time = time.time()
        runCalculate(tmp+target, tmp+result)
        print(f'\n\nProcessing finished in {time.time() - current_time} seconds')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "verification")
    parser.add_argument("target", type=str, help="Target file SLO (True)")
    parser.add_argument("result", type=str, help="Result from OCR (Check)")
    args = parser.parse_args()

    run(args.target, args.result)



