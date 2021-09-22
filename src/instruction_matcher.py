from typing import List

from .exceptions import InvalidInstructionException
from .models import ComplexOpcode, Mnemonic, Instruction


class InstructionMatcher:
    def __init__(self):
        # Dictionary of opcodes and matching instructions
        self._instruction_set = [
            Instruction(Mnemonic.ADD, [0x05, ComplexOpcode(0x81, opcode_extension=0), 0x01, 0x03]),
            Instruction(Mnemonic.AND, [0x25, ComplexOpcode(0x81, opcode_extension=4), 0x21, 0x23]),
            Instruction(Mnemonic.CALL, [0xe8, ComplexOpcode(0xff, opcode_extension=2)]),
            Instruction(Mnemonic.CALL_FLUSH, [ComplexOpcode(0x0f, next_byte=0xae)]),
            Instruction(Mnemonic.COMPARE, [0x3d, ComplexOpcode(0x81, opcode_extension=7), 0x39, 0x3b]),
            Instruction(Mnemonic.DECREMENT, [ComplexOpcode(0xff, opcode_extension=1), *range(0x48, 0x4f + 1)]),
            Instruction(Mnemonic.SIGNED_DIVIDE, [ComplexOpcode(0xf7, opcode_extension=7)]),
            Instruction(Mnemonic.SIGNED_MULTIPLY, [ComplexOpcode(0xf7, opcode_extension=5), ComplexOpcode(0x0f, next_byte=0xaf), 0x69]),
            Instruction(Mnemonic.INCREMENT, [ComplexOpcode(0xff, opcode_extension=0), *range(0x40, 0x47 + 1)]),
            Instruction(Mnemonic.JUMP, [0xeb, 0xe9, ComplexOpcode(0xff, opcode_extension=4)]),
            Instruction(Mnemonic.JUMP_ZERO, [0x74, ComplexOpcode(0x0f, next_byte=0x84)]),
            Instruction(Mnemonic.JUMP_NOT_ZERO, [0x75, ComplexOpcode(0x0f, next_byte=0x85)]),
            Instruction(Mnemonic.LOAD_EFFECTIVE_ADDRESS, [0x8d]),
            Instruction(Mnemonic.MOVE, [*range(0xb8, 0xbf + 1), 0xc7, 0x89, 0x8b]),
            Instruction(Mnemonic.MOVE_STRING, [0xa5]),
            Instruction(Mnemonic.MULTIPLY, [ComplexOpcode(0xf7, opcode_extension=4)]),
            Instruction(Mnemonic.NEGATE, [ComplexOpcode(0xf7, opcode_extension=3)]),
            Instruction(Mnemonic.NO_OP, [0x90]),
            Instruction(Mnemonic.NOT, [ComplexOpcode(0xf7, opcode_extension=2)]),
            Instruction(Mnemonic.OR, [0x0d, ComplexOpcode(0x81, opcode_extension=1), 0x09, 0x0b]),
            Instruction(Mnemonic.OUTPUT_TO_PORT, [0xe7]),
            Instruction(Mnemonic.POP, [0x8f, *range(0x58, 0x5f + 1)]),
            Instruction(Mnemonic.PUSH, [ComplexOpcode(0xff, opcode_extension=6), *range(0x50, 0x57 + 1), 0x68]),
            Instruction(Mnemonic.REPNE_CMPSD, [0xf2]),
            Instruction(Mnemonic.RETURN_FAR, [0xcb, 0xca]),
            Instruction(Mnemonic.RETURN_NEAR, [0xc3, 0xc2]),
            Instruction(Mnemonic.SHIFT_ARITHMETIC_LEFT, [ComplexOpcode(0xd1, opcode_extension=4)]),
            Instruction(Mnemonic.SHIFT_ARITHMETIC_RIGHT, [ComplexOpcode(0xd1, opcode_extension=7)]),
            Instruction(Mnemonic.SHIFT_LOGICAL_RIGHT, [ComplexOpcode(0xd1, opcode_extension=5)]),
            Instruction(Mnemonic.SUBTRACT_WITH_BORROW, [0x1d, ComplexOpcode(0x81, opcode_extension=3), 0x19, 0x1b]),
            Instruction(Mnemonic.SUBTRACT, [0x2d, ComplexOpcode(0x81, opcode_extension=5), 0x29, 0x2b]),
            Instruction(Mnemonic.TEST, [0xa9, ComplexOpcode(0xf7, opcode_extension=0), 0x85]),
            Instruction(Mnemonic.EXCLUSIVE_OR, [0x35, ComplexOpcode(0x81, opcode_extension=6), 0x31, 0x33]),
        ]

    def get_matching_instructions(self, byte) -> List[Instruction]:
        matching_instructions = []

        for instruction in self._instruction_set:
            if (instruction.first_byte_matches_opcode(byte)):
                matching_instructions.append(instruction)

        return matching_instructions

    def get_matching_instruction(self, first_byte, second_byte) -> Instruction:
        matching_instructions = self.get_matching_instructions(first_byte)

        if not matching_instructions:
            return None

        for instruction in matching_instructions:
            if instruction.bytes_match_opcode(first_byte, second_byte):
                return instruction

        raise InvalidInstructionException('Encountered invalid instruction with no matching opcodes: {} {}'.format(hex(first_byte), hex(second_byte)))
