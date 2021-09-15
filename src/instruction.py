from typing import List
from .mnemonic import Mnemonic

class Instruction:
    def __init__(self, mnemonic: Mnemonic, opcodes: List) -> None:
        self.mnemonic = mnemonic
        self.opcodes = opcodes
