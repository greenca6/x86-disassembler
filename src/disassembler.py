from src.models.mnemonic import Mnemonic
from src.models.decoded_instruction import DecodedInstruction
from typing import List
from .models import Instruction
from .decoders import InstructionDecoder

from .instruction_matcher import InstructionMatcher

class Disassembler:
    def disassemble(self, bytes):
        self._matcher = InstructionMatcher()
        self._decoder = InstructionDecoder(bytes)
        byte_index = 0
        instructions = []

        while byte_index < len(bytes):
            current_byte = bytes[byte_index]
            matching_instructions = self._matcher.get_matching_instructions(current_byte)

            # Instruction is unknown - keep going
            if len(matching_instructions) == 0:
                byte_index += 1
                continue
            
            matching_instruction: Instruction = None

            # Find the matching instruction via opcode. If more than one instruction shares the same opcode, read the next byte,
            # which could be a MOD R/M byte or just a lengthy opcode, to find the unique instruction
            if len(matching_instructions) == 1:
                matching_instruction = matching_instructions[0]
            elif len(matching_instructions) > 1:
                next_byte = bytes[byte_index + 1]
                matching_instruction = self._matcher.get_matching_instruction(current_byte, next_byte)

            # TODO: how to handle the scenario where no matching instruction is found at this point?

            decoded_instruction = self._decoder.decode_instruction(byte_index, matching_instruction.mnemonic)

            instructions.append(decoded_instruction)

            byte_index += len(decoded_instruction.bytes)

        # Instructions have now been disassembled - now we add any potential jump labels and output the results
        self._output_results(instructions)

    def _output_results(self, instructions: List[DecodedInstruction]):
        instruction_counter = 0

        for i in instructions:
            ic_location = '%08x' % instruction_counter
            output = ic_location + ':  ' + str(i)
            print(output)
            instruction_counter += len(i.bytes)

    def _get_offset_label(current_ic: int, instruction: DecodedInstruction) -> str:
        # check for instruction type, return None if not matching
        # break into two categories: rel8 and rel32
        if instruction.mnemonic not in [Mnemonic.JUMP, Mnemonic.JUMP_NOT_ZERO, Mnemonic.JUMP_ZERO, Mnemonic.CALL]:
            return None
        
        opcode = instruction.bytes[0]
        extended_opcode = instruction.bytes[1]

        # jz, jnz, jmp rel8 instructions
        if opcode in [0x74, 0x75, 0xeb]:
            # First sign-extend the rel8 number

            pass

        # rel32 instructions
        if (opcode == 0x0f and extended_opcode in [0x84, 0x85]) or (opcode in [0xe8, 0xe9]):
            last4_bytes = instruction.bytes[-4:]
            last4_bytes.reverse()
            rel32 = int(''.join(map(lambda b: '%02X' % b, last4_bytes)), 16)
            offset = current_ic + instruction.bytes + rel32
            return 'offset_{}'.format('%08x' % offset)

        # Non-deterministic jump/calls fall through and are decoded as-is
        return None
