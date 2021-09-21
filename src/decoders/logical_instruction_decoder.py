from src.models.instruction_signature import InstructionSignature
from ..models import Mnemonic, DecodedInstruction, Register

from .base_decoder import BaseDecoder


class LogicalInstructionDecoder(BaseDecoder):
    """
    Decoder that handles logical or boolean operations such as or, xor, sal, etc.
    """
    def decode_instruction(self, byte_index, mnemonic: Mnemonic) -> DecodedInstruction:
        if mnemonic == Mnemonic.AND:
            return self._decode_and(byte_index)
        elif mnemonic == Mnemonic.COMPARE:
            return self._decode_compare(byte_index)
        elif mnemonic == Mnemonic.NEGATE:
            return self._decode_negate(byte_index)
        elif mnemonic == Mnemonic.NOT:
            return self._decode_not(byte_index)
        elif mnemonic == Mnemonic.OR:
            return self._decode_or(byte_index)
        elif mnemonic == Mnemonic.SHIFT_ARITHMETIC_LEFT:
            return self._decode_shift_arithmetic_left(byte_index)
        elif mnemonic == Mnemonic.SHIFT_LOGICAL_RIGHT:
            return self._decode_shift_arithmetic_right(byte_index)
        elif mnemonic == Mnemonic.SHIFT_LOGICAL_RIGHT:
            return self._decode_shift_logical_right(byte_index)
        elif mnemonic == Mnemonic.TEST:
            return self._decode_test(byte_index)
        elif mnemonic == Mnemonic.EXCLUSIVE_OR:
            return self._decode_exclusive_or(byte_index)

        raise Exception('Attemted to decode instruction {} with the wrong decoder.'.format(mnemonic))
    
    def _decode_and(self, byte_index) -> DecodedInstruction:
        byte = self.bytes[byte_index]
        instruction = [Mnemonic.AND]

        # and eax, imm32
        if byte == 0x25:
            instruction.append(Register.to_string(Register.EAX))
            instruction.append(self.get_next_n_bytes(byte_index + 1, 4))
            return DecodedInstruction(instruction, self.bytes[byte_index:byte_index+5])
        # and r/m32, imm32
        elif byte == 0x81:
            return self.decode_instruction_by_signature(byte_index, InstructionSignature.RM32_IMM32, Mnemonic.AND, opcode_extension=4)
        # and r/m32, r32
        elif byte == 0x21:
            return self.decode_instruction_by_signature(byte_index, InstructionSignature.RM32_R32, Mnemonic.AND)
        # and r32, r/m32
        elif byte == 0x23:
            return self.decode_instruction_by_signature(byte_index, InstructionSignature.R32_RM32, Mnemonic.AND)

        raise Exception('Unable to decode and with given opcode: {}'.format(hex(byte)))

    def _decode_compare(self, byte_index) -> DecodedInstruction:
        byte = self.bytes[byte_index]
        instruction = [Mnemonic.COMPARE]

        # cmp eax, imm32
        if byte == 0x3d:
            instruction.append(Register.to_string(Register.EAX))
            instruction.append(self.get_next_n_bytes(byte_index + 1, 4))
            return DecodedInstruction(instruction, 6)
        # cmp r/m32, imm32
        elif byte == 0x81:
            return self.decode_instruction_by_signature(byte_index, InstructionSignature.RM32_IMM32, Mnemonic.COMPARE, opcode_extension=7)
        # cmp r/m32, r32
        elif byte == 0x39:
            return self.decode_instruction_by_signature(byte_index, InstructionSignature.RM32_R32, Mnemonic.COMPARE)
        # cmp r32, r/m32
        elif byte == 0x3b:
            return self.decode_instruction_by_signature(byte_index, InstructionSignature.R32_RM32, Mnemonic.COMPARE)

        raise Exception('Unable to decode cmp with given opcode: {}'.format(hex(byte)))

    def _decode_negate(self, byte_index) -> DecodedInstruction:
        byte = self.bytes[byte_index]

        if byte == 0xf7:
            return self.decode_instruction_by_signature(byte_index, InstructionSignature.RM32, Mnemonic.NEGATE, opcode_extension=3)

        raise Exception('Unable to decode neg with given opcode: {}'.format(hex(byte)))

    def _decode_not(self, byte_index) -> DecodedInstruction:
        byte = self.bytes[byte_index]

        if byte == 0xf7:
            return self.decode_instruction_by_signature(byte_index, InstructionSignature.RM32, Mnemonic.NOT, opcode_extension=2)

        raise Exception('Unable to decode not with given opcode: {}'.format(hex(byte)))

    def _decode_or(self, byte_index) -> DecodedInstruction:
        byte = self.bytes[byte_index]
        instruction = [Mnemonic.OR]

        # or eax, imm32
        if byte == 0x0d:
            instruction.append(Register.to_string(Register.EAX))
            instruction.append(self.get_next_n_bytes(byte_index + 1, 4))
            return DecodedInstruction(instruction, self.bytes[byte_index:byte_index+5])
        # or r/m32, imm32
        elif byte == 0x81:
            return self.decode_instruction_by_signature(byte_index, InstructionSignature.RM32_IMM32, Mnemonic.OR, opcode_extension=1)
        # or r/m32, r32
        elif byte == 0x09:
            return self.decode_instruction_by_signature(byte_index, InstructionSignature.RM32_R32, Mnemonic.OR)
        # or r32, r/m32
        elif byte == 0x0b:
            return self.decode_instruction_by_signature(byte_index, InstructionSignature.R32_RM32, Mnemonic.OR)

        raise Exception('Unable to decode or with given opcode: {}'.format(hex(byte)))

    def _decode_shift_arithmetic_left(self, byte_index) -> DecodedInstruction:
        byte = self.bytes[byte_index]

        if byte == 0xd1:
            # We need to read an extra byte at the end of the instruction after processing the r/m32 parameter
            i = self.decode_instruction_by_signature(byte_index, InstructionSignature.RM32, Mnemonic.SHIFT_ARITHMETIC_LEFT, opcode_extension=4)
            next_byte = self.bytes[byte_index + len(i.bytes) + 1]
            i.instruction.append(next_byte)
            return DecodedInstruction(i.instruction, self.bytes[byte_index:byte_index + len(i.bytes) + 1])

        raise Exception('Unable to decode sal with given opcode: {}'.format(hex(byte)))

    def _decode_shift_arithmetic_right(self, byte_index) -> DecodedInstruction:
        byte = self.bytes[byte_index]

        if byte == 0xd1:
            # We need to read an extra byte at the end of the instruction after processing the r/m32 parameter
            i = self.decode_instruction_by_signature(byte_index, InstructionSignature.RM32, Mnemonic.SHIFT_ARITHMETIC_LEFT, opcode_extension=7)
            next_byte = self.bytes[byte_index + len(i.bytes) + 1]
            i.instruction.append(next_byte)
            return DecodedInstruction(i.instruction, self.bytes[byte_index:byte_index + len(i.bytes) + 1])

        raise Exception('Unable to decode sal with given opcode: {}'.format(hex(byte)))

    def _decode_shift_logical_right(self, byte_index) -> DecodedInstruction:
        byte = self.bytes[byte_index]

        if byte == 0xd1:
            # We need to read an extra byte at the end of the instruction after processing the r/m32 parameter
            i = self.decode_instruction_by_signature(byte_index, InstructionSignature.RM32, Mnemonic.SHIFT_ARITHMETIC_LEFT, opcode_extension=7)
            next_byte = self.bytes[byte_index + len(i.bytes) + 1]
            i.instruction.append(next_byte)
            return DecodedInstruction(i.instruction, self.bytes[byte_index:byte_index + len(i.bytes) + 1])

        raise Exception('Unable to decode sal with given opcode: {}'.format(hex(byte)))

    def _decode_test(self, byte_index) -> DecodedInstruction:
        byte = self.bytes[byte_index]
        instruction = [Mnemonic.TEST]

        # test eax, imm32
        if byte == 0xa9:
            instruction.append(Register.to_string(Register.EAX))
            instruction.append(self.get_next_n_bytes(byte_index + 1, 4))
            return DecodedInstruction(instruction, self.bytes[byte_index:byte_index+5])
        # test r/m32, imm32
        elif byte == 0xf7:
            return self.decode_instruction_by_signature(byte_index, InstructionSignature.RM32_IMM32, Mnemonic.TEST, opcode_extension=0)
        # test r/m32, r32
        elif byte == 0x85:
            return self.decode_instruction_by_signature(byte_index, InstructionSignature.RM32_R32, Mnemonic.TEST)

        raise Exception('Unable to decode test with given opcode: {}'.format(hex(byte)))

    def _decode_exclusive_or(self, byte_index) -> DecodedInstruction:
        byte = self.bytes[byte_index]
        instruction = [Mnemonic.EXCLUSIVE_OR]

        # xor eax, imm32
        if byte == 0x35:
            instruction.append(Register.to_string(Register.EAX))
            instruction.append(self.get_next_n_bytes(byte_index + 1, 4))
            return DecodedInstruction(instruction, self.bytes[byte_index:byte_index+5])
        # xor r/m32, imm32
        elif byte == 0x81:
            return self.decode_instruction_by_signature(byte_index, InstructionSignature.RM32_IMM32, Mnemonic.EXCLUSIVE_OR, opcode_extension=6)
        # xor r/m32, r32
        elif byte == 0x31:
            return self.decode_instruction_by_signature(byte_index, InstructionSignature.RM32_R32, Mnemonic.EXCLUSIVE_OR)
        # xor r32, r/m32
        elif byte == 0x33:
            return self.decode_instruction_by_signature(byte_index, InstructionSignature.R32_RM32, Mnemonic.EXCLUSIVE_OR)

        raise Exception('Unable to decode xor with given opcode: {}'.format(hex(byte)))
