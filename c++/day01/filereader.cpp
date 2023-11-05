
#include "filereader.h"
#include <fstream>
#include <iostream>

// Constructor
Filereader::Filereader() {
    filesize = 0;
    filedata = nullptr;
}

// Destructor
Filereader::~Filereader() {
    if (filedata != nullptr) {
        delete[] filedata;
    }
}

// Read file and store data in filedata
int Filereader::read_file(const char* filename) {
    std::ifstream file(filename, std::ios::binary | std::ios::ate);
    if (!file.is_open()) {
        std::cerr << "Error opening file: " << filename << std::endl;
        return -1;
    }
    filesize = file.tellg();
    file.seekg(0, std::ios::beg);
    filedata = new char[filesize];
    file.read(filedata, filesize);
    file.close();

    // Ensure null-termination
    filedata[filesize] = '\0';

    return 0;
}

// Get filesize
int Filereader::get_filesize() {
    return filesize;
}

// Get filedata
char* Filereader::get_filedata() {
    return filedata;
}
