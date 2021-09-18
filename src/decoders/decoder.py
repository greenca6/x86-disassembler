from src.models.decoded_instruction import DecodedInstruction
from ..models import Mnemonic

from .arithmetic_instruction_decoder import ArithmeticInstructionDecoder
from .control_flow_instruction_decoder import ControlFlowInstructionDecoder
from .logical_instruction_decoder import LogicalInstructionDecoder
from .misc_instruction_decoder import MiscInstructionDecoder


class InstructionDecoder:
    def __init__(self, bytes) -> None:
        self.bytes = bytes
        self._arithmetic_instruction_decoder = ArithmeticInstructionDecoder(self.bytes)
        self._control_flow_instruction_decoder = ControlFlowInstructionDecoder(self.bytes)
        self._logical_instruction_decoder = LogicalInstructionDecoder(self.bytes)
        self._misc_instruction_decoder = MiscInstructionDecoder(self.bytes)

        self._arithmetic_mnemonics = [
            Mnemonic.ADD,
            Mnemonic.DECREMENT,
            Mnemonic.SIGNED_DIVIDE,
            Mnemonic.SIGNED_MULTIPLY,
            Mnemonic.INCREMENT,
            Mnemonic.MULTIPLY,
            Mnemonic.SUBTRACT_WITH_BORROW,
            Mnemonic.SUBTRACT,
        ]
        self._contrl_flow_mnemonics = [
            Mnemonic.CALL,
            Mnemonic.CALL_FLUSH,
            Mnemonic.JUMP,
            Mnemonic.JUMP_ZERO,
            Mnemonic.JUMP_NOT_ZERO,
            Mnemonic.RETURN_FAR,
            Mnemonic.RETURN_NEAR,
        ]
        self._logical_mnemonics = [
            Mnemonic.AND,
            Mnemonic.COMPARE,
            Mnemonic.NEGATE,
            Mnemonic.NOT,
            Mnemonic.OR,
            Mnemonic.SHIFT_ARITHMETIC_LEFT,
            Mnemonic.SHIFT_ARITHMETIC_RIGHT,
            Mnemonic.SHIFT_LOGICAL_RIGHT,
            Mnemonic.TEST,
            Mnemonic.EXCLUSIVE_OR,
        ]
        self._misc_mnemonics = [
            Mnemonic.LOAD_EFFECTIVE_ADDRESS,
            Mnemonic.MOVE,
            Mnemonic.MOVE_STRING,
            Mnemonic.NO_OP,
            Mnemonic.OUTPUT_TO_PORT,
            Mnemonic.POP,
            Mnemonic.PUSH,
            Mnemonic.REPNE_CMPSD,
        ]

    def decode_instruction(self, byte_index, mnemonic: Mnemonic) -> DecodedInstruction:
        if mnemonic in self._arithmetic_mnemonics:
            return self._arithmetic_instruction_decoder.decode_instruction(byte_index, mnemonic)
        elif mnemonic in self._contrl_flow_mnemonics:
            return self._control_flow_instruction_decoder.decode_instruction(byte_index, mnemonic)
        elif mnemonic in self._logical_mnemonics:
            return self._logical_instruction_decoder.decode_instruction(byte_index, mnemonic)
        elif mnemonic in self._misc_mnemonics:
            return self._misc_instruction_decoder.decode_instruction(byte_index, mnemonic)

        raise Exception('Attempted to decode an instruction. Mnemonic has no decoder: {}'.format(mnemonic))
