#ifndef _LISTING_WRITER_H_
#define _LISTING_WRITER_H_
#include <iostream>
#include <fstream>
#include <iomanip>
#include <vector>
#include "BinarySegment.hpp"
#include "Nodes.h"
using namespace std;
namespace ListingWriter {

		void writeFile(vector<BinarySegment*>& segments, std::string& filename, std::string sourceFile);
		


};





#endif