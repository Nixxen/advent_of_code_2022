#ifndef FILEREADER_H
#define FILEREADER_H

// Filereader class
class Filereader {
    public:
        Filereader();
        ~Filereader();
        int read_file(const char* filename);
        int get_filesize();
        char* get_filedata();
    private:
        int filesize;
        char* filedata;
};


#endif