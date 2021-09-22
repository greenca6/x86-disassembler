from typing import List

from src.models.mnemonic import Mnemonic

class DecodedInstruction:
    def __init__(self, instruction: List[str], bytes: List[int]) -> None:
        self.instruction = instruction
        self.bytes = bytes

    @property
    def mnemonic(self) -> Mnemonic:
        return self.instruction[0]

    @property
    def machine_code(self):
        return ''.join(map(lambda b: '%02X' % b, self.bytes))

    def __str__(self) -> str:
        return self.machine_code.ljust(24) + ' '.join(self.instruction)
