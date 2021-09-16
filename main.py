import sys

from src import Disassembler, disassembler


def getfile(filename):	
    with open(filename, 'rb') as f:
        a = f.read()
    return a	

def main():
    if len(sys.argv) < 2:
        print ("Please enter filename.")
        sys.exit(0)
    else:
        binary = getfile(sys.argv[1])

    disassembler = Disassembler()
    disassembler.disassemble(binary)

if __name__ == '__main__':
    main()
