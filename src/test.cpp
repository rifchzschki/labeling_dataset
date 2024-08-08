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
    cout << pattern.length()<<endl;
    return (double)lcs(str, pattern)/pattern.length();
}

int main(){
    string S1 = "Jalan ganesha 10 Institut Teknologi Bandung";
    string S2 = "Jalan ganosha 10 Instltut Teknologl Bandung";

    cout << lcs(S1, S2) << endl;
    // cout << S1.length() << endl;
    // cout << S2.length() << endl;
    cout << precisionString(S2, S1) << endl;

}