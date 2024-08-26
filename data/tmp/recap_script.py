import os
import re
import csv

def process_file(filename):
    total_hmean = 0
    total_entries = 0
    valid_count = 0
    
    with open(filename, 'r') as file:
        print(filename)
        for line in file:
            if line.startswith('Hmean:'):
                hmean = float(re.search(r'Hmean: ([\d.]+)', line).group(1))
                total_hmean += hmean
                total_entries += 1
            elif line.strip() == 'Valid':
                valid_count += 1
    
    avg_hmean = total_hmean / total_entries if total_entries > 0 else 0
    valid_ratio = valid_count / total_entries if total_entries > 0 else 0
    
    return avg_hmean, valid_ratio

def main():
    results = []
    
    for filename in os.listdir('.'):
        if filename.startswith('hasil_') and filename.endswith('.txt'):
            method = filename[6:-4]  
            avg_hmean, valid_ratio = process_file(filename)
            results.append([method, avg_hmean, valid_ratio])
    
    results.sort(key=lambda x: x[0])
    
    with open('results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Method', 'Hmean', 'Valid Ratio'])
        print(results)
        writer.writerows(results)

if __name__ == '__main__':
    main()