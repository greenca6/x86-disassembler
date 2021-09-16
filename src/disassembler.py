from .models import Instruction
from .parsers import InstructionParser

from .instruction_matcher import InstructionMatcher

class Disassembler:
    def __init__(self) -> None:
        self._matcher = InstructionMatcher()
        self._parser = InstructionParser()

    def disassemble(self, bytes):
        counter = 0
        instructions = {}

        while counter < len(bytes):
            current_byte = bytes[counter]
            matching_instructions = self._matcher.get_matching_instructions(current_byte)

            if len(matching_instructions) == 0:
                # Need to handle the special case here where we interpret this unknown instruction as `db <hex>`
                pass
            
            matching_instruction: Instruction = None

            if len(matching_instructions) == 1:
                matching_instruction = matching_instructions[0]
            elif len(matching_instructions) > 1 and counter + 1 < len(bytes):
                next_byte = bytes[counter + 1]
                matching_instruction = self._matcher.get_matching_instruction(current_byte, next_byte)

            parsed_instruction = self._parser.parse_instruction(bytes, current_byte, matching_instruction.mnemonic)

            counter += 1