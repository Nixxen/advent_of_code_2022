#include <iostream>
#include <fstream>
#include <vector>
#include <sstream>
#include "filereader.h"


using namespace std;

int main()
{
    // Read file
    Filereader fr;
    int result = fr.read_file("input.txt");
    if (result != 0) {
        cerr << "Error reading file" << endl;
        return -1;
    }
    int filesize = fr.get_filesize();
    char* filedata = fr.get_filedata();

    // Parse filedata
    vector<int> numbers;
    stringstream ss;

    for (int i = 0; i < filesize; i++) {
        if (filedata[i] == '\n') {
            numbers.push_back(stoi(ss.str()));
            ss.str("");
        } else {
            ss << filedata[i];
        }
    }

    // Print 
    for (int i = 0; i < numbers.size(); i++) {
        cout << numbers[i] << endl;
    }

    return 0;
}