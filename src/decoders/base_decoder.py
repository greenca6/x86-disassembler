from abc import ABC, abstractmethod
from src.exceptions.invalid_instruction_exception import InvalidInstructionException
from typing import List

from ..models import Mnemonic, DecodedInstruction, InstructionSignature, Register
from ..exceptions import BytesOutOfBoundsException

class BaseDecoder(ABC):
    def __init__(self, bytes: List[int]) -> None:
        self.bytes = bytes

    @abstractmethod
    def decode_instruction(self, byte_index, mnemonic: Mnemonic) -> DecodedInstruction:
        raise Exception('decode_instruction must be overridden by a subclass.')

    def decode_instruction_by_signature(self, instruction_byte_index: int, signature: InstructionSignature, mnemonic: Mnemonic, opcode_extension = None) -> DecodedInstruction:
        """
        Many instructions have a very similar signature to them, allowing us to reuse the decoding logic.

        instruction_byte_index: the index of the byte that starts this instruction
        signature: the instruction signature (one of: r/m32 imm32, r/m32 r32, r32 r/m32)
        mnemonic: the name of the instruction to decode
        opcode_extension: the optional opcode extension field, used for the r/m32, imm32 instruction signature only
        """
        instruction = [mnemonic]
        modrm_byte = self.get_raw_byte(instruction_byte_index + 1)
        (mod, reg, rm) = self.get_modrm_bits(modrm_byte)

        if signature == InstructionSignature.RM32:
            rm_register = Register.from_int(rm)

            # The REG field is assumed to be the opcode extension here - if this hits we're in trouble
            if reg != opcode_extension:
                raise InvalidInstructionException('Attempted to decode a {} instruction, but recieved an invalid reg value: {}'.format(mnemonic, reg))

            if mod == 0:
                # [r/m]
                if rm == Register.EBP:
                    disp32 = self.get_next_n_bytes(instruction_byte_index + 2, 4)
                    instruction.append('[{}]'.format(disp32))
                    return DecodedInstruction(instruction, self.bytes[instruction_byte_index:instruction_byte_index + 6])
                
                instruction.append('[{}]'.format(rm_register))
                return DecodedInstruction(instruction, self.bytes[instruction_byte_index:instruction_byte_index+2])
            elif mod == 1:
                # [r/m + 1-byte offset]
                offset = self.get_next_n_bytes(instruction_byte_index + 2, 1)
                instruction.append('[{} + {}]'.format(rm_register, offset))
                return DecodedInstruction(instruction, self.bytes[instruction_byte_index:instruction_byte_index+3])
            elif mod == 2:
                # [r/m + 4-byte offset]
                offset = self.get_next_n_bytes(instruction_byte_index + 2, 4)
                instruction.append('[{} + {}]'.format(rm_register, offset))
                return DecodedInstruction(instruction, self.bytes[instruction_byte_index:instruction_byte_index+6])
            elif mod == 3:
                # Direct register access, no need to do anything
                instruction.append('{}'.format(rm_register))
                return DecodedInstruction(instruction, self.bytes[instruction_byte_index:instruction_byte_index+2])
        elif signature == InstructionSignature.RM32_IMM32:
            rm_register = Register.from_int(rm)

            # The REG field is assumed to be the opcode extension here - if this hits we're in trouble
            if reg != opcode_extension:
                raise InvalidInstructionException('Attempted to decode a(n) {} instruction, but recieved an invalid reg value: {}'.format(mnemonic, reg))

            if mod == 0:
                # [r/m], imm32
                if rm == Register.EBP:
                    disp32 = self.get_next_n_bytes(instruction_byte_index + 2, 4)
                    imm = self.get_next_n_bytes(instruction_byte_index + 7, 4)
                    instruction.append('[{}],'.format(disp32))
                    instruction.append(imm)
                    return DecodedInstruction(instruction, self.bytes[instruction_byte_index:instruction_byte_index + 10])
                
                imm = self.get_next_n_bytes(instruction_byte_index + 2, 4)
                instruction.append('[{}],'.format(rm_register))
                instruction.append(imm)
                return DecodedInstruction(instruction, self.bytes[instruction_byte_index:instruction_byte_index+6])
            elif mod == 1:
                # [r/m + 1-byte offset], imm32
                offset = self.get_next_n_bytes(instruction_byte_index + 2, 1)
                imm = self.get_next_n_bytes(instruction_byte_index + 3, 4)
                instruction.append('[{} + {}],'.format(rm_register, offset))
                instruction.append(imm)
                return DecodedInstruction(instruction, self.bytes[instruction_byte_index:instruction_byte_index+7])
            elif mod == 2:
                # [r/m + 4-byte offset], imm32
                offset = self.get_next_n_bytes(instruction_byte_index + 2, 4)
                imm = self.get_next_n_bytes(instruction_byte_index + 6, 4)
                instruction.append('[{} + {}],'.format(rm_register, offset))
                instruction.append(imm)
                return DecodedInstruction(instruction, self.bytes[instruction_byte_index:instruction_byte_index+10])
            elif mod == 3:
                # Direct register access, no need to do anything
                imm = self.get_next_n_bytes(instruction_byte_index + 2, 4)
                instruction.append('{},'.format(rm_register))
                instruction.append(imm)
                return DecodedInstruction(instruction, self.bytes[instruction_byte_index:instruction_byte_index+6])
        elif signature == InstructionSignature.RM32_R32:
            reg_register = Register.from_int(reg)
            rm_register = Register.from_int(rm)
            
            if mod == 0:
                # [r/m], r32
                if rm == Register.EBP:
                    disp32 = self.get_next_n_bytes(instruction_byte_index + 2, 4)
                    instruction.append('[{}],'.format(disp32))
                    instruction.append(reg_register)
                    return DecodedInstruction(instruction, self.bytes[instruction_byte_index:instruction_byte_index + 6])

                instruction.append('[{}],'.format(rm_register))
                instruction.append(reg_register)
                return DecodedInstruction(instruction, self.bytes[instruction_byte_index:instruction_byte_index+2])
            elif mod == 1:
                # [r/m + 1-byte offset], reg
                offset = self.get_next_n_bytes(instruction_byte_index + 2, 1)
                instruction.append('[{} + {}],'.format(rm_register, offset))
                instruction.append(reg_register)
                return DecodedInstruction(instruction, self.bytes[instruction_byte_index:instruction_byte_index+3])
            elif mod == 2:
                # [r/m + 4-byte offset], reg
                offset = self.get_next_n_bytes(instruction_byte_index + 2, 4)
                instruction.append('[{} + {}],'.format(rm_register, offset))
                instruction.append(reg_register)
                return DecodedInstruction(instruction, self.bytes[instruction_byte_index:instruction_byte_index+6])
            elif mod == 3:
                # r/m, reg
                instruction.append('{},'.format(rm_register))
                instruction.append(reg_register)
                return DecodedInstruction(instruction, self.bytes[instruction_byte_index:instruction_byte_index+2])
        elif signature == InstructionSignature.R32_RM32:
            reg_register = Register.from_int(reg)
            rm_register = Register.from_int(rm)
            
            if mod == 0:
                # r32, [r/m]
                if rm == Register.EBP:
                    disp32 = self.get_next_n_bytes(instruction_byte_index + 2, 4)
                    instruction.append('{},'.format(reg_register))
                    instruction.append('[{}]'.format(disp32))
                    return DecodedInstruction(instruction, self.bytes[instruction_byte_index:instruction_byte_index + 6])
                
                instruction.append('{},'.format(reg_register))
                instruction.append('[{}]'.format(rm_register))
                return DecodedInstruction(instruction, self.bytes[instruction_byte_index:instruction_byte_index+2])
            elif mod == 1:
                # [r/m + 1-byte offset], reg
                offset = self.get_next_n_bytes(instruction_byte_index + 2, 1)
                instruction.append('{},'.format(reg_register))
                instruction.append('[{} + {}]'.format(rm_register, offset))
                return DecodedInstruction(instruction, self.bytes[instruction_byte_index:instruction_byte_index+3])
            elif mod == 2:
                # [r/m + 4-byte offset], reg
                offset = self.get_next_n_bytes(instruction_byte_index + 2, 4)
                instruction.append('{},'.format(reg_register))
                instruction.append('[{} + {}]'.format(rm_register, offset))
                return DecodedInstruction(instruction, self.bytes[instruction_byte_index:instruction_byte_index+6])
            elif mod == 3:
                # r/m, reg
                instruction.append('{},'.format(reg_register))
                instruction.append('{}'.format(rm_register))
                return DecodedInstruction(instruction, self.bytes[instruction_byte_index:instruction_byte_index+2])
        elif signature == InstructionSignature.R32_RM32_IMM:
            reg_register = Register.from_int(reg)
            rm_register = Register.from_int(rm)
            total_instructions = 2
            
            if mod == 0:
                if rm == Register.EBP:
                    disp32 = self.get_next_n_bytes(instruction_byte_index + 2, 4)
                    instruction.append('{},'.format(reg_register))
                    instruction.append('[{}],'.format(disp32))
                    total_instructions += 4
                else:
                    instruction.append('{},'.format(reg_register))
                    instruction.append('[{}],'.format(rm_register))
            elif mod == 1:
                # [r/m + 1-byte offset], reg
                offset = self.get_next_n_bytes(instruction_byte_index + 2, 1)
                instruction.append('{},'.format(reg_register))
                instruction.append('[{} + {}],'.format(rm_register, offset))
                total_instructions += 1
            elif mod == 2:
                # [r/m + 4-byte offset], reg
                offset = self.get_next_n_bytes(instruction_byte_index + 2, 4)
                instruction.append('{},'.format(reg_register))
                instruction.append('[{} + {}],'.format(rm_register, offset))
                total_instructions += 4
            elif mod == 3:
                # r/m, reg
                instruction.append('{},'.format(reg_register))
                instruction.append('{},'.format(rm_register))

            imm = self.get_next_n_bytes(instruction_byte_index + total_instructions, 4)
            instruction.append(imm)
            total_instructions += 4
            return DecodedInstruction(instruction, self.bytes[instruction_byte_index:instruction_byte_index + total_instructions])

        raise Exception('Unknown instruction signature: {}'.format(signature))

    def get_modrm_bits(self, modrm_byte) -> int:
        """
        returns the MOD, REG and RM values from the MOD R/M byte
        """
        mod = (modrm_byte & 0xc0) >> 6
        reg = (modrm_byte & 0x38) >> 3
        rm = (modrm_byte & 0x07)

        return (mod, reg, rm)

    def get_next_n_bytes(self, byte_index: int, n: int) -> str:
        """
        Returns the little-endian corrected version of the next n bytes.

        Example:
        Input: 44 33 22 11
        Output for byte_index=0, n=4: 0x11223344
        """
        bytes = []
        for i in range (n):
            if byte_index + i >= len(self.bytes):
                raise BytesOutOfBoundsException()

            bytes.append(self.bytes[byte_index + i])

        bytes.reverse()
        bytes = map(lambda b: '%02X' % b, bytes)
        bytes = ''.join(bytes)

        return '0x{}'.format(bytes)

    def get_raw_byte(self, byte_index: int) -> int:
        """
        Gets the raw byte at the specified index.
        """

        if byte_index >= len(self.bytes):
            raise BytesOutOfBoundsException()
        
        return self.bytes[byte_index]
