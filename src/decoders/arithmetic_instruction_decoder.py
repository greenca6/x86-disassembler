from src.models.register import Register
from ..models import Mnemonic, DecodedInstruction

from .base_decoder import BaseDecoder


class ArithmeticInstructionDecoder(BaseDecoder):
    """
    Decoder that handles add, subtract, multiply, divide, etc instructions.
    """
    def decode_instruction(self, byte_index, mnemonic: Mnemonic) -> DecodedInstruction:
        if mnemonic == Mnemonic.ADD:
            return self._decode_add(byte_index)
        elif mnemonic == Mnemonic.DECREMENT:
            return self._decode_decrement(byte_index)
        elif mnemonic == Mnemonic.SIGNED_DIVIDE:
            return self._decode_signed_divide(byte_index)
        elif mnemonic == Mnemonic.SIGNED_MULTIPLY:
            return self._decode_signed_multiply(byte_index)
        elif mnemonic == Mnemonic.INCREMENT:
            return self._decode_increment(byte_index)
        elif mnemonic == Mnemonic.MULTIPLY:
            return self._decode_multiply(byte_index)
        elif mnemonic == Mnemonic.SUBTRACT_WITH_BORROW:
            return self._decode_subtract_with_borrow(byte_index)
        elif mnemonic == Mnemonic.SUBTRACT:
            return self._decode_subtract(byte_index)

        raise Exception('Attemted to decode instruction {} with the wrong decoder.'.format(mnemonic))

    def _decode_add(self, byte_index: int) -> DecodedInstruction:
        byte = self.bytes[byte_index]
        instruction = [Mnemonic.ADD]

        # add eax, imm32
        if byte == 0x05:
            instruction.append(Register.to_string(Register.EDX))
            instruction.append(self.get_next_n_bytes(byte_index + 1, 4))
            return DecodedInstruction(instruction, 6)
        # add r/m32, imm32
        elif byte == 0x81:
            modrm_byte = self.bytes[byte_index + 1]
            (mod, reg, rm) = self.get_modrm_bits(modrm_byte)
            rm_register = Register.from_int(rm)

            # The REG field is assumed to be 0 here - if this hits we're in trouble
            if reg != 0:
                raise Exception('Attempted to decode an add instruction with opcode 0x81, but recieved an invalid reg value: {}'.format(reg))

            if mod == 0:
                # [r/m], imm32
                imm = self.get_next_n_bytes(byte_index + 2, 4)
                instruction.append('[{}],'.format(rm_register))
                instruction.append(imm)
                return DecodedInstruction(instruction, 6)
            elif mod == 1:
                # [r/m + 1-byte offset], imm32
                offset = self.get_next_n_bytes(byte_index + 2, 1)
                imm = self.get_next_n_bytes(byte_index + 3, 4)
                instruction.append('[{} + {}],'.format(rm_register, offset))
                instruction.append(imm)
                return DecodedInstruction(instruction, 7)
            elif mod == 2:
                # [r/m + 4-byte offset], imm32
                offset = self.get_next_n_bytes(byte_index + 2, 4)
                imm = self.get_next_n_bytes(byte_index + 6, 4)
                instruction.append('[{} + {}],'.format(rm_register, offset))
                instruction.append(imm)
                return DecodedInstruction(instruction, 10)
            elif mod == 3:
                # Direct register access, no need to do anything
                imm = self.get_next_n_bytes(byte_index + 2, 4)
                instruction.append('{},'.format(rm_register))
                instruction.append(imm)
                return DecodedInstruction(instruction, 6)
        # add r/m32, r32
        elif byte == 0x01:
            modrm_byte = self.bytes[byte_index + 1]
            (mod, reg, rm) = self.get_modrm_bits(modrm_byte)
            reg_register = Register.from_int(reg)
            rm_register = Register.from_int(rm)
            
            if mod == 0:
                instruction.append('[{}],'.format(rm_register))
                instruction.append(reg_register)
                return DecodedInstruction(instruction, 2)
            elif mod == 1:
                # [r/m + 1-byte offset], reg
                offset = self.get_next_n_bytes(byte_index + 2, 1)
                instruction.append('[{} + {}],'.format(rm_register, offset))
                instruction.append(reg_register)
                return DecodedInstruction(instruction, 3)
            elif mod == 2:
                # [r/m + 4-byte offset], reg
                offset = self.get_next_n_bytes(byte_index + 2, 4)
                instruction.append('[{} + {}],'.format(rm_register, offset))
                instruction.append(reg_register)
                return DecodedInstruction(instruction, 6)
            elif mod == 3:
                # r/m, reg
                instruction.append('{},'.format(rm_register))
                instruction.append(reg_register)
                return DecodedInstruction(instruction, 2)
        # add r32, r/m32
        elif byte == 0x03:
            modrm_byte = self.bytes[byte_index + 1]
            (mod, reg, rm) = self.get_modrm_bits(modrm_byte)
            reg_register = Register.from_int(reg)
            rm_register = Register.from_int(rm)
            
            if mod == 0:
                instruction.append('{},'.format(reg_register))
                instruction.append('[{}]'.format(rm_register))
                return DecodedInstruction(instruction, 2)
            elif mod == 1:
                # [r/m + 1-byte offset], reg
                offset = self.get_next_n_bytes(byte_index + 2, 1)
                instruction.append('{},'.format(reg_register))
                instruction.append('[{} + {}]'.format(rm_register, offset))
                return DecodedInstruction(instruction, 3)
            elif mod == 2:
                # [r/m + 4-byte offset], reg
                offset = self.get_next_n_bytes(byte_index + 2, 4)
                instruction.append('{},'.format(reg_register))
                instruction.append('[{} + {}]'.format(rm_register, offset))
                return DecodedInstruction(instruction, 6)
            elif mod == 3:
                # r/m, reg
                instruction.append('{},'.format(reg_register))
                instruction.append('{}'.format(rm_register))
                return DecodedInstruction(instruction, 2)

        raise Exception('Unable to decode add with given opcode: {}'.format(hex(byte)))

    def _decode_decrement(self, byte_index: int) -> DecodedInstruction:
        pass

    def _decode_signed_divide(self, byte_index: int) -> DecodedInstruction:
        pass

    def _decode_signed_multiply(self, byte_index: int) -> DecodedInstruction:
        pass

    def _decode_increment(self, byte_index: int) -> DecodedInstruction:
        pass

    def _decode_multiply(self, byte_index: int) -> DecodedInstruction:
        pass

    def _decode_subtract_with_borrow(self, byte_index: int) -> DecodedInstruction:
        pass

    def _decode_subtract(self, byte_index: int) -> DecodedInstruction:
        pass