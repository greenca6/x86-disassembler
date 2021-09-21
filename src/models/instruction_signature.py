from enum import Enum

class InstructionSignature(Enum):
    RM32_IMM32 = 0
    RM32_R32 = 1
    R32_RM32 = 2
    RM32 = 3
    R32_RM32_IMM = 4
