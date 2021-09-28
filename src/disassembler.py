from typing import List

from .exceptions import BytesOutOfBoundsException, InvalidInstructionException
from .models import Mnemonic, DecodedInstruction, Instruction
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
                instructions.append(DecodedInstruction([Mnemonic.DB, '0x%02x' % current_byte], bytes[byte_index:byte_index+1]))
                byte_index += 1
                continue
            
            matching_instruction: Instruction = None

            # Find the matching instruction via opcode. If more than one instruction shares the same opcode, read the next byte,
            # which could be a MOD R/M byte or just a lengthy opcode, to find the unique instruction
            if len(matching_instructions) == 1:
                matching_instruction = matching_instructions[0]
            elif len(matching_instructions) > 1:
                # Edge case where we are expecting more bits but don't have any to read
                if byte_index + 1 >= len(bytes):
                    instructions.append(DecodedInstruction([Mnemonic.DB, '0x%02x' % current_byte], bytes[byte_index:byte_index+1]))
                    byte_index += 1
                    continue

                next_byte = bytes[byte_index + 1]
                matching_instruction = self._matcher.get_matching_instruction(current_byte, next_byte)

            if matching_instruction == None:
                instructions.append(DecodedInstruction([Mnemonic.DB, '0x%02x' % current_byte], bytes[byte_index:byte_index+1]))
                byte_index += 1
                continue

            try:
                decoded_instruction = self._decoder.decode_instruction(byte_index, matching_instruction.mnemonic)
            except (BytesOutOfBoundsException, InvalidInstructionException):
                instructions.append(DecodedInstruction([Mnemonic.DB, '0x%02x' % current_byte], bytes[byte_index:byte_index+1]))
                byte_index += 1
                continue

            instructions.append(decoded_instruction)

            byte_index += len(decoded_instruction.bytes)

        # Instructions have now been disassembled - now we add any potential jump labels and output the results
        self._output_results(instructions)

    def _output_results(self, instructions: List[DecodedInstruction]):
        instruction_counter = 0
        labels = {}

        # First loop through the program to find/calculate any labels that may exist
        for i in instructions:
            offset_label = self._get_offset_label(instruction_counter, i)

            # Add the calculated label to the dictionary if it exists, and modify the instruction containing the label
            if offset_label:
                labels = { **labels, **offset_label }
                label = list(offset_label.values())[0]
                i.instruction = [*i.instruction[:-1], label]

            instruction_counter += len(i.bytes)

        instruction_counter = 0
        # Finally loop through the program and print out the full thing
        for i in instructions:
            ic_location = '%08x' % instruction_counter

            label = labels.get(instruction_counter)

            if label:
                print('{}:'.format(label))

            print(ic_location + ':  ' + str(i))
            instruction_counter += len(i.bytes)

    def _get_offset_label(self, current_ic: int, instruction: DecodedInstruction):
        if instruction.mnemonic not in [Mnemonic.JUMP, Mnemonic.JUMP_NOT_ZERO, Mnemonic.JUMP_ZERO, Mnemonic.CALL]:
            return None
        
        opcode = instruction.bytes[0]
        extended_opcode = instruction.bytes[1]

        # jz, jnz, jmp rel8 instructions
        if opcode in [0x74, 0x75, 0xeb]:
            # First sign-extend the rel8 number
            last_byte = instruction.bytes[-1]
            sign_extended = 0xffffff00 | last_byte if last_byte >= 0x80 else last_byte
            offset = current_ic + len(instruction.bytes) + sign_extended
            
            # Drop the 33rd bit if it exists
            if offset > 0xffffffff:
                offset = offset - 0x100000000

            return { offset: 'offset_{}'.format('%08x' % offset) }
        # rel32 instructions
        elif (opcode == 0x0f and extended_opcode in [0x84, 0x85]) or (opcode in [0xe8, 0xe9]):
            last4_bytes = list(instruction.bytes[-4:])
            last4_bytes.reverse()
            rel32 = int(''.join(map(lambda b: '%02X' % b, last4_bytes)), 16)
            offset = current_ic + len(instruction.bytes) + rel32

            # Drop the 33rd bit if it exists
            if offset > 0xffffffff:
                offset = offset - 0x100000000

            return { offset: 'offset_{}'.format('%08x' % offset) }

        # Non-deterministic jump/calls fall through and are decoded as-is
        return None
