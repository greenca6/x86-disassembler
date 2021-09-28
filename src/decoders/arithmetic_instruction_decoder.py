from src.models.instruction_signature import InstructionSignature
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
            instruction.append(Register.from_int(Register.EAX))
            instruction.append(self.get_next_n_bytes(byte_index + 1, 4))
            return DecodedInstruction(instruction, self.bytes[byte_index:byte_index+5])
        # add r/m32, imm32
        elif byte == 0x81:
            return self.decode_instruction_by_signature(byte_index, InstructionSignature.RM32_IMM32, Mnemonic.ADD, opcode_extension=0)
        # add r/m32, r32
        elif byte == 0x01:
            return self.decode_instruction_by_signature(byte_index, InstructionSignature.RM32_R32, Mnemonic.ADD)
        # add r32, r/m32
        elif byte == 0x03:
            return self.decode_instruction_by_signature(byte_index, InstructionSignature.R32_RM32, Mnemonic.ADD)

        raise Exception('Unable to decode add with given opcode: {}'.format(hex(byte)))

    def _decode_decrement(self, byte_index: int) -> DecodedInstruction:
        byte = self.bytes[byte_index]
        instruction = [Mnemonic.DECREMENT]

        if byte in range(0x48, 0x48 + 8):
            target_register = Register.from_int(byte - 0x48)
            instruction.append('{}'.format(target_register))
            return DecodedInstruction(instruction, self.bytes[byte_index:byte_index + 1])
        elif byte == 0xff:
            return self.decode_instruction_by_signature(byte_index, InstructionSignature.RM32, Mnemonic.DECREMENT, opcode_extension=1)
        
        raise Exception('Unable to decode dec with given opcode: {}'.format(hex(byte)))

    def _decode_signed_divide(self, byte_index: int) -> DecodedInstruction:
        byte = self.bytes[byte_index]

        if byte == 0xf7:
            return self.decode_instruction_by_signature(byte_index, InstructionSignature.RM32, Mnemonic.SIGNED_DIVIDE, opcode_extension=7)

        raise Exception('Unable to decode idiv with given opcode: {}'.format(hex(byte)))

    def _decode_signed_multiply(self, byte_index: int) -> DecodedInstruction:
        byte = self.bytes[byte_index]

        if byte == 0xf7:
            return self.decode_instruction_by_signature(byte_index, InstructionSignature.RM32, Mnemonic.SIGNED_MULTIPLY, opcode_extension=5)
        elif byte == 0x0f:
            next_byte = self.get_raw_byte(byte_index + 1)

            if next_byte != 0xaf:
                raise Exception('Unable to decode imul with given opcode: {}{}'.format(hex(byte), hex(next_byte)))

            # This instruction has an extra byte in it's opcode so we have to modify the return results from the decode_instruction call
            i = self.decode_instruction_by_signature(byte_index + 1, InstructionSignature.R32_RM32, Mnemonic.SIGNED_MULTIPLY)
            return DecodedInstruction(i.instruction, self.bytes[byte_index:byte_index+len(i.bytes) + 1])
        elif byte == 0x69:
            return self.decode_instruction_by_signature(byte_index, InstructionSignature.R32_RM32_IMM, Mnemonic.SIGNED_MULTIPLY)

        raise Exception('Unable to decode idiv with given opcode: {}'.format(hex(byte)))


    def _decode_increment(self, byte_index: int) -> DecodedInstruction:
        byte = self.bytes[byte_index]
        instruction = [Mnemonic.INCREMENT]

        if byte in range(0x40, 0x40 + 8):
            target_register = Register.from_int(byte - 0x40)
            instruction.append('{}'.format(target_register))
            return DecodedInstruction(instruction, self.bytes[byte_index:byte_index+1])
        elif byte == 0xff:
            return self.decode_instruction_by_signature(byte_index, InstructionSignature.RM32, Mnemonic.INCREMENT, opcode_extension=0)

        raise Exception('Unable to decode inc with given opcode: {}'.format(hex(byte)))

    def _decode_multiply(self, byte_index: int) -> DecodedInstruction:
        byte = self.bytes[byte_index]

        if byte == 0xf7:
            return self.decode_instruction_by_signature(byte_index, InstructionSignature.RM32, Mnemonic.MULTIPLY, opcode_extension=4)

        raise Exception('Unable to decode mul with given opcode: {}'.format(hex(byte)))

    def _decode_subtract_with_borrow(self, byte_index: int) -> DecodedInstruction:
        byte = self.bytes[byte_index]
        instruction = [Mnemonic.SUBTRACT_WITH_BORROW]

        # sub eax, imm32
        if byte == 0x1d:
            instruction.append(Register.from_int(Register.EAX))
            instruction.append(self.get_next_n_bytes(byte_index + 1, 4))
            return DecodedInstruction(instruction, self.bytes[byte_index:byte_index+5])
        # sub r/m32, imm32
        elif byte == 0x81:
            return self.decode_instruction_by_signature(byte_index, InstructionSignature.RM32_IMM32, Mnemonic.SUBTRACT_WITH_BORROW, opcode_extension=3)
        # sub r/m32, r32
        elif byte == 0x19:
            return self.decode_instruction_by_signature(byte_index, InstructionSignature.RM32_R32, Mnemonic.SUBTRACT_WITH_BORROW)
        # sub r32, r/m32
        elif byte == 0x1b:
            return self.decode_instruction_by_signature(byte_index, InstructionSignature.R32_RM32, Mnemonic.SUBTRACT_WITH_BORROW)

        raise Exception('Unable to decode sbb with given opcode: {}'.format(hex(byte)))

    def _decode_subtract(self, byte_index: int) -> DecodedInstruction:
        byte = self.bytes[byte_index]
        instruction = [Mnemonic.SUBTRACT]

        # sub eax, imm32
        if byte == 0x2d:
            instruction.append(Register.from_int(Register.EAX))
            instruction.append(self.get_next_n_bytes(byte_index + 1, 4))
            return DecodedInstruction(instruction, self.bytes[byte_index:byte_index+5])
        # sub r/m32, imm32
        elif byte == 0x81:
            return self.decode_instruction_by_signature(byte_index, InstructionSignature.RM32_IMM32, Mnemonic.SUBTRACT, opcode_extension=3)
        # sub r/m32, r32
        elif byte == 0x29:
            return self.decode_instruction_by_signature(byte_index, InstructionSignature.RM32_R32, Mnemonic.SUBTRACT)
        # sub r32, r/m32
        elif byte == 0x2b:
            return self.decode_instruction_by_signature(byte_index, InstructionSignature.R32_RM32, Mnemonic.SUBTRACT)

        raise Exception('Unable to decode sub with given opcode: {}'.format(hex(byte)))