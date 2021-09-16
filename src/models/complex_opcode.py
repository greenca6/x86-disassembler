class ComplexOpcode:
    """
    A 'Complex' Opcode is one that cannot be determined solely by the first byte. A second byte must be read to determine if a given
    byte matches this opcode.

    A few examples where if we were to look solely at the first byte, we would match other instructions:
    1. clflush m8 (0x0f 0xae)
    2. sal r/m32, 1 (0xd1 /1)

    byte: the first byte in this opcode to determine if the instruction is a match
    next_byte: the optional next byte used to uniquely identify this instruction
    opcode_extension: the optional opcode extension (base 10) which represents the REG field in the MODR/M byte (the second byte in the overall instruction)
    """
    def __init__(self, byte, next_byte: int = None, opcode_extension: int = None) -> None:
        if (next_byte is not None and opcode_extension is not None):
            raise Exception('Cannot create a variable opcode with both a next_byte and opcode_extension, pick one or the other, not both.')
        if next_byte is None and opcode_extension is None:
            raise Exception('Must set either a next_byte or opcode_extension.')

        self.byte = byte
        self.next_byte = next_byte
        self.opcode_extension = opcode_extension

    def matches_first_byte(self, byte):
        return self.byte == byte

    def matches_next_byte(self, second_byte):
        if self.next_byte:
            return self.next_byte == second_byte

        # Grab the reg value, return true if the one we have matches the one given
        reg = (second_byte & 0x38) >> 3
    
        return reg == self.opcode_extension
