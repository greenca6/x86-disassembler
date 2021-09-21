from ..models import Mnemonic, DecodedInstruction, InstructionSignature, Register

from .base_decoder import BaseDecoder


class MiscInstructionDecoder(BaseDecoder):
    """
    Decocder that handles all other instructions that aren't handled by the other decoders.
    """
    def decode_instruction(self, byte_index, mnemonic: Mnemonic) -> DecodedInstruction:
        if mnemonic == Mnemonic.LOAD_EFFECTIVE_ADDRESS:
            return self._decode_load_effective_address(byte_index)
        elif mnemonic == Mnemonic.MOVE:
            return self._decode_move(byte_index)
        elif mnemonic == Mnemonic.MOVE_STRING:
            return self._decode_move_string(byte_index)
        elif mnemonic == Mnemonic.NO_OP:
            return self._decode_no_op(byte_index)
        elif mnemonic == Mnemonic.OUTPUT_TO_PORT:
            return self._decode_output_to_port(byte_index)
        elif mnemonic == Mnemonic.POP:
            return self._decode_pop(byte_index)
        elif mnemonic == Mnemonic.PUSH:
            return self._decode_push(byte_index)
        elif mnemonic == Mnemonic.REPNE_CMPSD:
            return self._decode_repne_cmpsd(byte_index)

        raise Exception('Attemted to decode instruction {} with the wrong decoder.'.format(mnemonic))

    def _decode_load_effective_address(self, byte_index) -> DecodedInstruction:
        byte = self.bytes[byte_index]

        if byte in range(0x8d, 0x8d + 8):
            return self.decode_instruction_by_signature(byte_index, InstructionSignature.R32_RM32, Mnemonic.LOAD_EFFECTIVE_ADDRESS)

        raise Exception('Unable to decode lea with given opcode: {}'.format(hex(byte)))

    def _decode_move(self, byte_index) -> DecodedInstruction:
        byte = self.bytes[byte_index]
        instruction = [Mnemonic.MOVE]

        # mov r32, imm32
        if byte in range(0xb8, 0xbf + 1):
            target_register = Register.from_int(byte - 0xb8)
            instruction.append('{},'.format(target_register))
            instruction.append(self.get_next_n_bytes(byte_index + 1, 4))
            return DecodedInstruction(instruction, self.bytes[byte_index:byte_index+5])
        # mov r/m32, imm32
        elif byte == 0xc7:
            return self.decode_instruction_by_signature(byte_index, InstructionSignature.RM32_IMM32, Mnemonic.MOVE, opcode_extension=0)
        # mov r/m32, r32
        elif byte == 0x89:
            return self.decode_instruction_by_signature(byte_index, InstructionSignature.RM32_R32, Mnemonic.MOVE)
        # mov r32, r/m32
        elif byte == 0x8b:
            return self.decode_instruction_by_signature(byte_index, InstructionSignature.R32_RM32, Mnemonic.MOVE)

        raise Exception('Unable to decode mov with given opcode: {}'.format(hex(byte)))

    def _decode_move_string(self, byte_index) -> DecodedInstruction:
        byte = self.bytes[byte_index]
        instruction = [Mnemonic.MOVE_STRING]

        if byte == 0xa5:
            return DecodedInstruction(instruction, self.bytes[byte_index:byte_index + 1])

        raise Exception('Unable to decode movsd with given opcode: {}'.format(hex(byte)))

    def _decode_no_op(self, byte_index) -> DecodedInstruction:
        byte = self.bytes[byte_index]
        instruction = [Mnemonic.NO_OP]

        if byte == 0x90:
            return DecodedInstruction(instruction, self.bytes[byte_index:byte_index + 1])

        raise Exception('Unable to decode nop with given opcode: {}'.format(hex(byte)))

    def _decode_output_to_port(self, byte_index) -> DecodedInstruction:
        byte = self.bytes[byte_index]
        instruction = [Mnemonic.OUTPUT_TO_PORT]

        if byte == 0xe7:
            imm = self.get_next_n_bytes(byte_index + 1, 1)
            instruction.append('{},'.format(imm))
            instruction.append('eax')
            return DecodedInstruction(instruction, self.bytes[byte_index:byte_index + 2])

        raise Exception('Unable to decode out with given opcode: {}'.format(hex(byte)))

    def _decode_pop(self, byte_index) -> DecodedInstruction:
        byte = self.bytes[byte_index]
        instruction = [Mnemonic.POP]

        if byte == 0x8f:
            return self.decode_instruction_by_signature(byte_index, InstructionSignature.RM32, Mnemonic.POP, opcode_extension=0)
        elif byte in range(0x58, 0x5f + 1):
            target_register = Register.from_int(byte - 0x58)
            instruction.append(target_register)
            return DecodedInstruction(instruction, self.bytes[byte_index:byte_index+1])

        raise Exception('Unable to decode pop with given opcode: {}'.format(hex(byte)))

    def _decode_push(self, byte_index) -> DecodedInstruction:
        byte = self.bytes[byte_index]
        instruction = [Mnemonic.PUSH]

        if byte == 0xff:
            return self.decode_instruction_by_signature(byte_index, InstructionSignature.RM32, Mnemonic.PUSH, opcode_extension=6)
        elif byte in range(0x50, 0x57 + 1):
            target_register = Register.from_int(byte - 0x50)
            instruction.append(target_register)
            return DecodedInstruction(instruction, self.bytes[byte_index:byte_index+1])
        elif byte == 0x68:
            imm = self.get_next_n_bytes(byte_index + 1, 4)
            instruction.append(imm)
            return DecodedInstruction(instruction, self.bytes[byte_index:byte_index+5])

        raise Exception('Unable to decode push with given opcode: {}'.format(hex(byte)))


    def _decode_repne_cmpsd(self, byte_index) -> DecodedInstruction:
        byte = self.bytes[byte_index]
        opcode_extension = self.bytes[byte_index + 1]

        if byte == 0xf2 and opcode_extension == 0xa7:
            return DecodedInstruction([Mnemonic.REPNE_CMPSD], self.bytes[byte_index:byte_index + 2])

        raise Exception('Unable to decode repne cmpsd with given opcode: {}{}'.format(hex(byte), hex(opcode_extension)))

