from typing import List, Union

from .complex_opcode import ComplexOpcode
from .mnemonic import Mnemonic

class Instruction:
    def __init__(self, mnemonic: Mnemonic, opcodes: List[Union[int, ComplexOpcode]]) -> None:
        self.mnemonic = mnemonic
        self.opcodes = opcodes

    def first_byte_matches_opcode(self, byte: int) -> bool:
        """
        Returns true if the given byte matches any opcode that can be used with this Instruction.
        """
        for opcode in self.opcodes:
            if isinstance(opcode, ComplexOpcode) and opcode.matches_first_byte(byte):
                return True
            if opcode == byte:
                return True

        return False

    def bytes_match_opcode(self, first_byte, second_byte) -> bool:
        """
        Returns true if the given byte matches any opcode that can be used with this Instruction, looking solely at the instructions'
        variable opcodes (opcodes that can have an extension or second byte identifier).
        """
        for opcode in self.opcodes:
            if isinstance(opcode, ComplexOpcode):
                if opcode.matches_first_byte(first_byte) and opcode.matches_next_byte(second_byte):
                    return True

        return False
