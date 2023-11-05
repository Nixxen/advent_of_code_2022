#include <iostream>
#include <fstream>
#include <string>
#include <cmath>
using namespace std;

int main()
{
    ifstream input;
    input.open("day1_input.txt");
    string s;
    int mx, cur;
    while (!input.eof())
    {
        getline(input, s);
        if (s != "")
            cur += stoi(s);
        else
            mx = max(mx, cur), cur = 0;
    }
    cout << mx << endl;
    return 0;
}