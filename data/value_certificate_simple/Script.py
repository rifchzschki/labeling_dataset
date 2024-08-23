name = {
    "Boemi": [1, 2, 4, 6, 7, 10, 12, 15, 18, 23],
    "Dahruji": [90, 91, 92, 93, 94, 95, 96, 97, 98, 99],
    "Didi": [80, 81, 82, 83, 84, 85, 86, 87, 88, 89],
    "Henry": [60, 61, 62, 63, 64, 65, 66, 67, 68, 69],
    "InstalasiRumahTangga": [51, 52, 53, 54, 55, 56, 58],
    "Jumali": [11, 13, 21, 22, 24, 29, 30, 31, 32, 42, 44],
    "Kasmuji": [8, 9, 19, 20, 27, 28, 39],
    "Lisman": [70, 71, 72, 73, 74, 75, 76, 77, 78, 79],
    "Prapto": [3, 5, 14, 16, 17, 25, 26,  33, 36, 45, 46, 57],
    "WarungSimpangTiga": [34, 35, 37, 38, 41, 43, 47, 48, 49, 50],
}

for each in name:
    with open(each + ".txt", 'r') as file1:
        content = file1.read()
    for nameFile in name[each]:
        with open("../value_sip/"+ str(nameFile) + ".txt", 'w') as file2:
            file2.write(content)
        