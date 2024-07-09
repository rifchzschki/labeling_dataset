import json
import os

# Path ke direktori tempat file-file Anda disimpan
directory = 'label'

# Fungsi untuk memproses setiap file
def process_files(filename):
    filepath = os.path.join(directory, filename)
    with open(filepath, 'r') as file:
        for line in file:
            if line.strip():  # Pastikan baris tidak kosong
                # Pisahkan nama file dari data JSON
                parts = line.split('\t', 1)
                if len(parts) == 2:
                    file_name, json_data = parts
                    json_data = json.loads(json_data)
                    for i, item in enumerate(json_data):
                        item['id'] = i + 1

                    # Add linking attribute
                    for i, item in enumerate(json_data):
                        linking = []
                        if item['key_cls'] == 'question':
                            j=i+1
                            print(json_data[j]['key_cls'])
                            while(json_data[j]['key_cls'] != 'question'):
                                if(json_data[j]['key_cls'] == 'answer'):
                                    linking.append([i+1, j+1])
                                    json_data[j]['linking'] = linking
                                    break
                                else:
                                    j+=1
                            item['linking'] = linking
                        elif(item['key_cls'] == 'other') :
                            item['linking'] = linking


                    # json_data = json.dumps(json_data)
                    yield file_name.strip(), json_data

# Contoh penggunaan
with open('label/final.txt', 'w') as out:
    for file_name, json_data in process_files("init.txt"):
        out.write(f"{file_name}\t{json.dumps(json_data)}\n")
#     json.dump(json_data, file, indent=4)
    print(f"File Name: {file_name}")
    # print(f"JSON Data:")
    # print(json.dumps(json_data, indent=4))
    print("\n")
