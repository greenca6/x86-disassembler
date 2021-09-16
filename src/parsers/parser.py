from ..models import Mnemonic

from .arithmetic_instruction_parser import ArithmeticInstructionParser
from .control_flow_instruction_parser import ControlFlowInstructionParser
from .logical_instruction_parser import LogicalInstructionParser
from .misc_instruction_parser import MiscInstructionParser


class InstructionParser:
    def __init__(self) -> None:
        self._arithmetic_instruction_parser = ArithmeticInstructionParser()
        self._control_flow_instruction_parser = ControlFlowInstructionParser()
        self._logical_instruction_parser = LogicalInstructionParser()
        self._misc_instruction_parser = MiscInstructionParser()

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

    def parse_instruction(self, binary, current_byte_index, mnemonic: Mnemonic):
        pass