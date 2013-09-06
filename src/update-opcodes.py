#!/usr/bin/python
import sys,os 

def run_parser(sFile):
	lines = []
	lut = {}
	f = open(sFile, 'r')
	lines = [line.strip() for line in f if (line[0] != '#' and line[0] != "/n")]
	lines = [line for line in lines if len(line) > 0]
	for index, line in enumerate(lines):
		tokens = [tok.strip() for tok in line.split()]
		if tokens[0] == "!def":
			lut[tokens[1]] = int(tokens[2], 0)
		elif tokens[0] == "!begin":
			helper_gen_files(lines[index+1:], lut)
			break
def helper_gen_files(lineset, lut):
	
	fheader = open("symtable-generated.hpp.tmp","w")

	opcodes = []
	#dict of indexes for each opcode starting location
	d = {}

	#write out the preamble

	idx = 0
	for lineCounter, line in enumerate(lineset):
		tableEntry = []		
		operandsIdx = -1
		params = [l.strip() for l in line.split(",")]
		if len(params[0]) > 0:
			opcodes.append(params[0])
			fheader.write("//" + opcodes[-1] + "\n");
			d[opcodes[-1]] = []

		d[opcodes[-1]].append([idx,-1])


		options = 0
		for opt in params[1].split():
			try:
				options = options | lut[opt.strip()]
			except KeyError:
				print "error! lookup {%s} value not found!" % opt
		tableEntry.append(options)
		
		opbyteStart = 2
		if options & lut["MODRM_EXT"]:
			tableEntry.append(int(params[2],0) << 3)
			opbyteStart = opbyteStart + 1

		for i,param in enumerate(params[opbyteStart:]):
			if param[0] == "r" or param[0] == "m" or param[0] == "i":
				operandsIdx = i + opbyteStart
				break
			else:
				tableEntry.append(int(param,0))
		
		operandCount = 0
		if operandsIdx != -1:
			for param in params[operandsIdx:]:
				byte = 0
				if param.find("@") != -1:
					#preset reg
					opts =[opt.strip() for opt in param.split("@")]
					byte = lut[opts[0]]
					byte = byte | (lut[opts[1]] << 5) | lut['REG_PRESET']
				else: #regular pipe separated values
					types = [argtype.strip() for argtype in param.split("|")]
					for argtype in types:
						byte = byte | lut[argtype]
				
				tableEntry.append(byte)
				operandCount = operandCount + 1

		tableEntry[0] = tableEntry[0] | operandCount
		fheader.write("\t")
		for byte in tableEntry[:-1]:
			fheader.write(str(byte) + ",")
		fheader.write(str(tableEntry[-1]))
		if (lineCounter + 1 != len(lineset)):
			 fheader.write(",")

		fheader.write("\n");
	
		idx = idx + len(tableEntry)
		d[opcodes[-1]][-1][1] = len(tableEntry)
	fheader.close()



	inst_variant_count = 0
	instr_index = 0
	fvars = open("symtable-generated.hpp.tmp.2","w")
	finstrs = open("symtable-generated.hpp.tmp.3","w")


	for key, valueList in sorted(d.iteritems()):
		#track number of variants per opcode
		v = 0
		iv_start = inst_variant_count
		for value in valueList:
			fvars.write("{" + str(value[1]) + ", " + "&bOpcodeTable[" + str(value[0]) + "]},\n")
			inst_variant_count = inst_variant_count + 1
			v = v + 1
		
		finstrs.write("{%d, &iVars[%d]},\n" % (v, iv_start))

	fvars.seek(fvars.tell() - 2)

	fvars.write(" ")
	finstrs.seek(finstrs.tell() - 2)
	finstrs.write(" ")
	finstrs.close()
	fvars.close()



	fheader_processed = open("symtable-generated.hpp", "w")
	fheader_processed.write(
		"""#ifndef SYMTABLE_GEN_H
#define SYMTABLE_GEN_H

typedef struct {
	int szVar; //size of the opcode byte array
	unsigned char* pStart; // pointer to the start of the array
} inst_variant;

typedef struct {
	int varCount; //number of variants
	inst_variant* ptr; //pointer to first element
} inst_t;

""")
	fheader_processed.write("static unsigned char bOpcodeTable[" + str(idx) + "] = {\n")	
	ftemp = open("symtable-generated.hpp.tmp","r")
	for l in ftemp:
		fheader_processed.write(l);
	ftemp.close()
	fheader_processed.write("\n};\n")

	fheader_processed.write("static inst_variant iVars[" + str(inst_variant_count) + "] = { \n")
	ftemp = open("symtable-generated.hpp.tmp.2","r")
	for l in ftemp:
		fheader_processed.write(l);
	ftemp.close()

	fheader_processed.write("\n};\n")

	fheader_processed.write("static inst_t instr[%d] = {\n" % len(opcodes))
	ftemp = open("symtable-generated.hpp.tmp.3","r")
	for l in ftemp:
		fheader_processed.write(l);
	ftemp.close()




	fheader_processed.write("};\n#endif\n")
	fheader_processed.close()

	os.remove("symtable-generated.hpp.tmp")
	os.remove("symtable-generated.hpp.tmp.2")
	os.remove("symtable-generated.hpp.tmp.3")



	## Lexer definition update!
	fLexer = open("p86asm.l","w")
	ftemp = open("p86asm.l.inc", "r")
	for l in ftemp:
		if l.find("%{/*OPCODES*/%}") != -1:
			for i, opcode in enumerate(opcodes):
				fLexer.write(opcodes[i] + '\t {yylval.pOpcode =(parser_opcode*) malloc(sizeof(parser_opcode)); yylval.pOpcode->pStr = strdup(yytext); yylval.pOpcode->instrID = %d; BEGIN(PARAM);\t return OPCODE;}\n' % i)
		else:
			fLexer.write(l)
	fLexer.write("\n%%")

	ftemp.close()
	fLexer.close()



if __name__ == "__main__":
	run_parser("opcodes.dat")