#include "VirgoWriter.h"
#include <iomanip>

#define DELIM "\x1f"
namespace VirgoWriter{

void writeFile(vector<BinarySegment*>& segments, string& filename, unsigned int startingAddress){
	int bytes_written = 0;
	clog << "Starting object-write process!" << endl; 
	ofstream outfile;		
	outfile.open (filename.c_str());
	Constant* label;
	 	
	outfile << "3 " << segments.size() << " " << startingAddress << "       " << endl;


	for (int i = 0; i < segments.size();i++){
		
		if (!segments[i])
			continue;
		outfile <<  DELIM;
		outfile << hex << setw(4) << setfill('0');
	    outfile << (unsigned short)segments[i]->getCounter() <<  DELIM;
		outfile << dec;
		outfile <<  "\x1f" << segments[i]->size() <<  "\x1f";
		bytes_written += segments[i]->size();
		outfile << "\x1f" << *segments[i] << "\x1f";
		outfile << "\x1f";
		
		if (segments[i]->getLabel())
			outfile << segments[i]->getLabel()->getContent();
		outfile << "\x1f";

		if (segments[i]->getStringData() != "")
			outfile << "\x1f" << segments[i]->getStringData() << "\x1f";
		else
		
			outfile << "\x1f" << "\x1f";
		outfile << "\x1f" << dec << 20 <<"\x1f" << endl;
		}

	
	outfile.seekp(0);
	outfile << "3 " << segments.size() << " " << dec << startingAddress << " " << bytes_written << " ";
	outfile.close();

}

};