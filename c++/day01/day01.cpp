#include <iostream>
#include <fstream>
#include <vector>
#include <sstream>
#include "filereader.h"

int main()
{
    // Read file
    Filereader fr;
    int result = fr.read_file("day01_input.txt");
    if (result != 0)
    {
        std::cerr << "Error reading file" << std::endl;
        return -1;
    }
    int filesize = fr.get_filesize();
    char *filedata = fr.get_filedata();

    // Find the Elf carrying the most Calories. How many total Calories is that Elf carrying?
    // Using newline to separate the data
    int mostCalories = 0;

    // Using stringstream to separate the data
    std::stringstream ss(filedata);
    std::string line;
    while (std::getline(ss, line))
    {
        int calories = std::stoi(line);
        mostCalories += calories;
    }
    std::cout << "The Elf carrying the most Calories is carrying " << mostCalories << " Calories." << std::endl;

    return 0;
}