from .mnemonic import Mnemonic
from .instruction import Instruction

class InstructionRepostory:
    # how to handle opcode overlaps for the first byte? Non unique opcodes:
    # 0x81
    # 0x0f
    # 0xd1
    # 0xf7
    # 0xff
    _instructionSet = [
        Instruction(Mnemonic.ADD, [0x05, 0x81, 0x01, 0x03]),
        Instruction(Mnemonic.AND, [0x25, 0x81, 0x21, 0x23]),
        Instruction(Mnemonic.CALL, [0xe8, 0xff]),
        Instruction(Mnemonic.CALL_FLUSH, [0x0f]),
        Instruction(Mnemonic.COMPARE, [0x3d, 0x81, 0x39, 0x3b]),
        Instruction(Mnemonic.DECREMENT, [0xff, 0x48, 0x49, 0x4a, 0x4b, 0x4c, 0x4d, 0x4e, 0x4f]), # opcode 0x48+rd is dynamic
        Instruction(Mnemonic.SIGNED_DIVIDE, [0xf7]),
        Instruction(Mnemonic.SIGNED_MULTIPLY, [0xf7, 0x0f, 0x69]),
        Instruction(Mnemonic.INCREMENT, [0xff, 0x40, 0x41, 0x42, 0x43, 0x44, 0x45, 0x46, 0x47]), # opcode 0x40+rd is dynamic
        Instruction(Mnemonic.JUMP, [0xeb, 0xe9, 0xff]),
        Instruction(Mnemonic.JUMP_ZERO, [0x74, 0x0f]),
        Instruction(Mnemonic.JUMP_NOT_ZERO, [0x75, 0x0f]),
        Instruction(Mnemonic.LOAD_EFFECTIVE_ADDRESS, [0x8d]),
        Instruction(Mnemonic.MOVE, [0xb8, 0xb9, 0xba, 0xbb, 0xbc, 0xbd, 0xbe, 0xbf, 0xc7, 0x89, 0x8b]), # opcode 0xB8+rd is dynamic
        Instruction(Mnemonic.MOVE_STRING, [0xa5]),
        Instruction(Mnemonic.MULTIPLY, [0xf7]),
        Instruction(Mnemonic.NEGATE, [0xf7]),
        Instruction(Mnemonic.NO_OP, [0x90]),
        Instruction(Mnemonic.NOT, [0xf7]),
        Instruction(Mnemonic.OR, [0x0d, 0x81, 0x09, 0x0b]),
        Instruction(Mnemonic.OUTPUT_TO_PORT, [0xe7]),
        Instruction(Mnemonic.POP, [0x8f, 0x58]), # opcode 0x58+rd is dynamic
        Instruction(Mnemonic.PUSH, [0xff, 0x50, 0x68]), # opcode 0x50+rd is dynamic
        Instruction(Mnemonic.REPNE_CMPSD, [0xf2]),
        Instruction(Mnemonic.RETURN_FAR, [0xcb, 0xca]),
        Instruction(Mnemonic.RETURN_NEAR, [0xc3, 0xc2]),
        Instruction(Mnemonic.SHIFT_ARITHMETIC_LEFT, [0xd1]),
        Instruction(Mnemonic.SHIFT_ARITHMETIC_RIGHT, [0xd1]),
        Instruction(Mnemonic.SHIFT_LOGICAL_RIGHT, [0xd1]),
        Instruction(Mnemonic.SUBTRACT_WITH_BORROW, [0x1d, 0x81, 0x19, 0x1b]),
        Instruction(Mnemonic.SUBTRACT, [0x2d, 0x81, 0x29, 0x2b]),
        Instruction(Mnemonic.TEST, [0xa9, 0xf7, 0x85]),
        Instruction(Mnemonic.EXCLUSIVE_OR, [0x35, 0x81, 0x31, 0x33]),
    ]

    def __init__(self) -> None:
        pass
