from .models import Instruction
from .decoders import InstructionDecoder

from .instruction_matcher import InstructionMatcher

class Disassembler:
    def disassemble(self, bytes):
        self._matcher = InstructionMatcher()
        self._decoder = InstructionDecoder(bytes)
        byte_index = 0
        instructions = {}

        while byte_index < len(bytes):
            current_byte = bytes[byte_index]
            matching_instructions = self._matcher.get_matching_instructions(current_byte)

            if len(matching_instructions) == 0:
                # Need to handle the special case here where we interpret this unknown instruction as `db <hex>`
                pass
            
            matching_instruction: Instruction = None

            if len(matching_instructions) == 1:
                matching_instruction = matching_instructions[0]
            elif len(matching_instructions) > 1:
                next_byte = bytes[byte_index + 1]
                matching_instruction = self._matcher.get_matching_instruction(current_byte, next_byte)

            decoded_instruction = self._decoder.decode_instruction(byte_index, matching_instruction.mnemonic)

            print(' '.join(decoded_instruction.instruction))

            byte_index += decoded_instruction.total_bytes
