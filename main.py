import sys

from src import Disassembler


def getfile(filename):	
    with open(filename, 'rb') as f:
        a = f.read()
    return a	

def main():
    if len(sys.argv) < 3:
        print ("Invalid command format. Valid format: `python main.py -i <input_file>`.")
        sys.exit(0)
    else:
        binary = getfile(sys.argv[2])

    disassembler = Disassembler()
    disassembler.disassemble(binary)

if __name__ == '__main__':
    main()
