#ifndef BINARYSEGMENT_H_
#define BINARYSEGMENT_H_
#include <string>
#include <stdint.h>
#include <stdlib.h>
#include <vector>
#include <iostream>
#include <iomanip>
#include "data.h"
#include "Nodes.h"


class BinarySegment{
	public:		
			BinarySegment();
			void push_back(uint8_t byte);
			void setUpdateFlag(bool isRel);
			void setConstant(Constant* cst);
			void setAddrSize(AccessWidth aw);
			int getAddrStartIndex();
			uint8_t& operator[] (int index);
			int size();
			void setCounter(unsigned int c);
			unsigned int getCounter();
			bool getUpdateFlag();
			Constant* getConstant();
			AccessWidth& getAddrSize();
			bool getRelativeAddressFlag();
			void setStringData(std::string a);
			std::string& getStringData();
			friend ostream& operator<<( ostream &output, const BinarySegment& src);
			void setLabel(LabelNode* p);
			LabelNode* getLabel();
			void setSourceNode(BaseExpressionNode* ptr);
			BaseExpressionNode* getSourceNode();

	private:
			vector<uint8_t> m_data;
			bool m_updateAddress;
			bool m_isRel;
			Constant* m_addr;
			AccessWidth m_addrSize;
			int m_addrStartIndex;
			int m_counter;
			string m_stringData;
			LabelNode* m_labelptr;
			BaseExpressionNode* m_exprptr;

};

#endif
