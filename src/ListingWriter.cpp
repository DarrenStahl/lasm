#include "ListingWriter.hpp"

namespace ListingWriter{

	
void writeFile(vector<BinarySegment*>& segments, std::string& filename, std::string sourceFile)
{
	char* pBuffer = NULL;
	char* writePos = NULL;
	char* writeStart = NULL;
	ofstream outfile;		
	int bytes_written = 0;
	int i = 0;
	int length;
	int curLineNo = 0;
	std::ifstream is (sourceFile.c_str(), std::ifstream::binary);
	if (is) {
    // get length of file:
    is.seekg (0, is.end);
    length = is.tellg();
    is.seekg (0, is.beg);

    pBuffer= new char[length+1];

    clog << "Reading " << length << " characters... ";
    // read data as a block:
    is.read (pBuffer,length);

    if (is)
      clog << "all characters read successfully.";
    else
      clog << "error: only " << is.gcount() << " could be read";
    is.close();
    //null terminate the buffer;
    pBuffer[length] = 0;
	//delete[] pBuffer;
	writePos = pBuffer;
	writeStart = pBuffer;
  }
	outfile.open (filename.c_str());


  	 while (bytes_written < length){
		
		while(*(writePos) != '\n' && *writePos != 0)
			writePos++;
		
		//EOF
		if (*writePos == 0)
			break;

		curLineNo++;

		int sz = writePos - writeStart;

				//skip past the newln
		writePos++;



		bool segments_written = false;
		while(i < segments.size() && segments[i] && (segments[i]->getSourceNode()->getLineNumber() == curLineNo)){
			outfile << setw(4) << setfill('0') << hex << segments[i]->getCounter()
			 << "\t" <<setw(5) << *segments[i] << "\t";
			i++;
			segments_written = true;
		}
		if (segments_written)
			outfile << "\t";
		else
			outfile << "\t\t\t\t\t";
		outfile.write(writeStart, sz);
		outfile << "\n";
		writeStart = writePos;
		bytes_written+= sz;
		

		}


		outfile.close();
		delete[] pBuffer;


	}
};