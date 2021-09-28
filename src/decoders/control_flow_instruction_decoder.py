from src.models.instruction_signature import InstructionSignature
from ..models import Mnemonic, DecodedInstruction, Register

from .base_decoder import BaseDecoder


class ControlFlowInstructionDecoder(BaseDecoder):
    """
    Decoder that handles control flow instructions such as jump, jnz, etc.
    """
    def decode_instruction(self, byte_index, mnemonic: Mnemonic) -> DecodedInstruction:
        if mnemonic == Mnemonic.CALL:
            return self._decode_call(byte_index)
        elif mnemonic == Mnemonic.CALL_FLUSH:
            return self._decode_call_flush(byte_index)
        elif mnemonic == Mnemonic.JUMP:
            return self._decode_jump(byte_index)
        elif mnemonic == Mnemonic.JUMP_ZERO:
            return self._decode_jump_zero(byte_index)
        elif mnemonic == Mnemonic.JUMP_NOT_ZERO:
            return self._decode_jump_not_zero(byte_index)
        elif mnemonic == Mnemonic.RETURN_FAR:
            return self._decode_return_far(byte_index)
        elif mnemonic == Mnemonic.RETURN_NEAR:
            return self._decode_return_near(byte_index)

        raise Exception('Attemted to decode instruction {} with the wrong decoder.'.format(mnemonic))

    def _decode_call(self, byte_index) -> DecodedInstruction:
        byte = self.bytes[byte_index]
        instruction = [Mnemonic.CALL]

        if byte == 0xe8:
            imm = self.get_next_n_bytes(byte_index + 1, 4)
            instruction.append(imm)
            return DecodedInstruction(instruction, self.bytes[byte_index:byte_index+5])
        elif byte == 0xff:
            return self.decode_instruction_by_signature(byte_index, InstructionSignature.RM32, Mnemonic.CALL, opcode_extension=2)

        raise Exception('Unable to decode call with given opcode: {}'.format(hex(byte)))
        

    def _decode_call_flush(self, byte_index) -> DecodedInstruction:
        byte = self.bytes[byte_index]
        next_byte = self.get_raw_byte(byte_index + 1)
        modrm_byte = self.get_raw_byte(byte_index + 2)
        (mod, reg, rm) = self.get_modrm_bits(modrm_byte)
        instruction = [Mnemonic.CALL_FLUSH]
        rm_register = Register.from_int(rm)

        if byte != 0x0f or next_byte != 0xae:
            raise Exception('Attempted to decode a clflush instruction, but recieved an invalid opcode: {}{}'.format(hex(byte), hex(next_byte)))

        if reg != 7:
            raise Exception('Attempted to decode a clflush instruction, but recieved an invalid reg value: {}'.format(reg))

        if mod == 3:
            raise Exception('Given an invalid addressing mode in the mod value: 11b')

        if mod == 0:
            # [r/m]
            if rm == Register.EBP:
                disp32 = self.get_next_n_bytes(byte_index + 2, 4)
                instruction.append('[{}]'.format(disp32))
                return DecodedInstruction(instruction, self.bytes[byte_index:byte_index + 7])
            else:
                instruction.append('[{}]'.format(rm_register))
                return DecodedInstruction(instruction, self.bytes[byte_index:byte_index + 3])
        elif mod == 1:
            # [r/m + 1-byte offset]
            offset = self.get_next_n_bytes(byte_index + 2, 1)
            instruction.append('[{} + {}]'.format(rm_register, offset))
            return DecodedInstruction(instruction, self.bytes[byte_index:byte_index+4])
        elif mod == 2:
            # [r/m + 4-byte offset]
            offset = self.get_next_n_bytes(byte_index + 1, 4)
            instruction.append('[{} + {}]'.format(rm_register, offset))
            return DecodedInstruction(instruction, self.bytes[byte_index:byte_index+7])


    def _decode_jump(self, byte_index) -> DecodedInstruction:
        byte = self.bytes[byte_index]
        instruction = [Mnemonic.JUMP]

        if byte == 0xeb:
            rel = self.get_next_n_bytes(byte_index + 1, 1)
            instruction.append(rel)
            return DecodedInstruction(instruction, self.bytes[byte_index:byte_index + 2])
        elif byte == 0xe9:
            rel = self.get_next_n_bytes(byte_index + 1, 4)
            instruction.append(rel)
            return DecodedInstruction(instruction, self.bytes[byte_index:byte_index + 5])
        elif byte == 0xff:
            return self.decode_instruction_by_signature(byte_index, InstructionSignature.RM32, Mnemonic.JUMP, opcode_extension=4)

        raise Exception('Unable to decode jmp with given opcode: {}'.format(hex(byte)))

    def _decode_jump_zero(self, byte_index) -> DecodedInstruction:
        byte = self.bytes[byte_index]
        instruction = [Mnemonic.JUMP_ZERO]

        if byte == 0x74:
            rel = self.get_next_n_bytes(byte_index + 1, 1)
            instruction.append(rel)
            return DecodedInstruction(instruction, self.bytes[byte_index:byte_index + 2])
        elif byte == 0x0f:
            next_byte = self.get_raw_byte(byte_index + 1)

            if next_byte != 0x84:
                raise Exception('Attempted to decode a jz instruction, but recieved an invalid opcode: {}{}'.format(hex(byte), hex(next_byte)))

            rel = self.get_next_n_bytes(byte_index + 2, 4)
            instruction.append(rel)
            return DecodedInstruction(instruction, self.bytes[byte_index:byte_index + 6])

        raise Exception('Unable to decode jz with given opcode: {}'.format(hex(byte)))

    def _decode_jump_not_zero(self, byte_index) -> DecodedInstruction:
        byte = self.bytes[byte_index]
        instruction = [Mnemonic.JUMP_NOT_ZERO]

        if byte == 0x75:
            rel = self.get_next_n_bytes(byte_index + 1, 1)
            instruction.append(rel)
            return DecodedInstruction(instruction, self.bytes[byte_index:byte_index + 2])
        elif byte == 0x0f:
            next_byte = self.get_raw_byte(byte_index + 1)

            if next_byte != 0x85:
                raise Exception('Attempted to decode a jnz instruction, but recieved an invalid opcode: {}{}'.format(hex(byte), hex(next_byte)))

            rel = self.get_next_n_bytes(byte_index + 2, 4)
            instruction.append(rel)
            return DecodedInstruction(instruction, self.bytes[byte_index:byte_index + 6])

        raise Exception('Unable to decode jnz with given opcode: {}'.format(hex(byte)))

    def _decode_return_far(self, byte_index) -> DecodedInstruction:
        byte = self.bytes[byte_index]
        instruction = [Mnemonic.RETURN_FAR]

        if byte == 0xcb:
            return DecodedInstruction(instruction, [self.bytes[byte_index]])
        elif byte == 0xca:
            imm = self.get_next_n_bytes(byte_index + 1, 2)
            instruction.append(imm)
            return DecodedInstruction(instruction, self.bytes[byte_index:byte_index+3])

        raise Exception('Unable to decode retf with given opcode: {}'.format(hex(byte)))

    def _decode_return_near(self, byte_index) -> DecodedInstruction:
        byte = self.bytes[byte_index]
        instruction = [Mnemonic.RETURN_NEAR]

        if byte == 0xc3:
            return DecodedInstruction(instruction, [self.bytes[byte_index]])
        elif byte == 0xc2:
            imm = self.get_next_n_bytes(byte_index + 1, 2)
            instruction.append(imm)
            return DecodedInstruction(instruction, self.bytes[byte_index:byte_index+3])

        raise Exception('Unable to decode retn with given opcode: {}'.format(hex(byte)))

