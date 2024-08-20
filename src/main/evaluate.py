import sys
import re

def lcs(text1, text2):
    n = len(text1)
    m = len(text2)

    prev = [0] * (m + 1)
    cur = [0] * (m + 1)

    for idx1 in range(1, n + 1):
        for idx2 in range(1, m + 1):
            if text1[idx1 - 1] == text2[idx2 - 1]:
                cur[idx2] = 1 + prev[idx2 - 1]
            else:
                cur[idx2] = max(cur[idx2 - 1], prev[idx2])
        prev = cur[:]

    return cur[m]

def precision_string(str, pattern):
    return lcs(str, pattern) / len(pattern)

def calculate_matrix(str_file_path, pattern_file_path):
    list_str = []
    list_pattern = []

    with open(str_file_path, 'r') as file:
        for line in file:
            print(line)
            list_pattern.append(remove_non_alphanumeric(line))
    
    with open(pattern_file_path, 'r') as file:
        for line in file:
            print(line)
            list_str.append(remove_non_alphanumeric(line))

    i = 0
    idx_found = 0
    prec_all = 0
    mul = 0
    isFake = False

    while i < len(list_pattern):
        prec = 0
        j = max(idx_found - 5, 0)

        while j < len(list_str):
            tmp_prec = precision_string(list_str[j], list_pattern[i])
            if prec < tmp_prec:
                # print(list_pattern[i])
                # print(list_str[j])
                prec = tmp_prec
                idx_found = j
            j += 1

        # print(list_pattern[i])
        # print(prec, "\n")

        if prec <= 0.5:
            isFake = True

        if i != 0:
            prec_all *= prec
            prec_all += mul
        else:
            mul = prec
            prec_all += 1

        mul *= prec
        i += 1

    # print("Hmean", mul * len(list_pattern) / prec_all)
    if(isFake):
        return (mul * len(list_pattern) / prec_all), ("Fake")
    else:
        return (mul * len(list_pattern) / prec_all), ("Valid")
    

def remove_non_alphanumeric(s):
    return re.sub(r'\W+', '', s)


