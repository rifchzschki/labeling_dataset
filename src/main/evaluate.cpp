#include <iostream>
#include <vector>
#include <fstream>
#include <string>
#include <cctype> 
#include <algorithm>
using namespace std;

int lcs(string& text1, string& text2)
{
    int n = text1.size();
    int m = text2.size();

    // initializing 2 vectors of size m
    vector<int> prev(m + 1, 0), cur(m + 1, 0);

    for (int idx2 = 0; idx2 < m + 1; idx2++)
        cur[idx2] = 0;

    for (int idx1 = 1; idx1 < n + 1; idx1++) {
        for (int idx2 = 1; idx2 < m + 1; idx2++) {
            // if matching
            if (text1[idx1 - 1] == text2[idx2 - 1])
                cur[idx2] = 1 + prev[idx2 - 1];

            // not matching
            else
                cur[idx2]
                    = 0 + max(cur[idx2 - 1], prev[idx2]);
        }
        prev = cur;
    }

    return cur[m];
}

double precisionString(string str, string pattern){
    // cout << str.size() << endl;
    // cout << pattern.size() << endl;
    return (double)lcs(str, pattern)/pattern.size();
}

void calculteMatrix(vector<string> listStr, vector<string> listPattern){
    int i=0, j=0, idxFound=0;
    double precAll=0;
    double mul=0;
    while(i<listPattern.size()){
        double prec=0;
        j = (idxFound>=5 ? idxFound-5 : 0);
        // cout << listPattern[i] << endl;
        // cout << listPattern[i].size() << endl;
        while(j<listStr.size()){
            double tmpPrec = precisionString(listStr[j], listPattern[i]); 
            if(prec<tmpPrec){
                // cout << tmpPrec << endl;
                cout << listPattern[i] << endl;
                cout << listStr[j] << endl;
                prec = tmpPrec; 
                idxFound = j;
            }
            j++;
        }
        cout << listPattern[i] << endl;
        cout << prec << endl << endl;

        if(prec<=0.5){
            cout << "Precision : 0 (Fake)";
            return;
        }
        if(i!=0){
            precAll*=prec;
            precAll+=mul;
        }else{
            mul=prec;
            precAll+=1;
        }
        mul*=prec;
        i++;
    }
    cout << "Precision " << mul*listPattern.size()/precAll;
}

int main(int argc, char* argv[]) {
    if (argc != 3) {
        cerr << "Usage: " << argv[0] << " <input_file_1> <input_file_2>" << endl;
        return 1;
    }

    ifstream inputFile1(argv[1]);
    ifstream inputFile2(argv[2]);

    if (!inputFile1) {
        cerr << "Could not open the file: " << argv[1] << endl;
        return 1;
    }

    if (!inputFile2) {
        cerr << "Could not open the file: " << argv[2] << endl;
        return 1;
    }

    vector<string> pattern;
    vector<string> ocrResult;
    string line;
    
    auto removeNonAlphanumeric = [](std::string& str) {
        str.erase(std::remove_if(str.begin(), str.end(), [](char c) {
            return !std::isalnum(c);
        }), str.end());
    };

    while (getline(inputFile1, line)) {
        removeNonAlphanumeric(line);
        pattern.push_back(line);
    }

    while (getline(inputFile2, line)) {
        removeNonAlphanumeric(line);
        ocrResult.push_back(line);
    }

    inputFile1.close();
    inputFile2.close();

    // Menampilkan list of strings yang diterima dari file 1
    // cout << "Received strings from file 1:" << endl;
    // for (const auto& str : pattern) {
    //     cout << str << endl;
    // }

    // // Menampilkan list of strings yang diterima dari file 2
    // cout << "Received strings from file 2:" << endl;
    // for (const auto& str : ocrResult) {
    //     cout << str << endl;
    // }
    calculteMatrix(ocrResult, pattern);


    return 0;
}
