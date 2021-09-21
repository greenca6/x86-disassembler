from typing import List


class DecodedInstruction:
    def __init__(self, instruction: List[str], bytes: List[int]) -> None:
        self.instruction = instruction
        self.bytes = bytes

    @property
    def machine_code(self):
        return ''.join(map(lambda b: hex(b).replace('0x', ''), self.bytes))

    def __str__(self) -> str:
        return self.machine_code.ljust(16) + ' '.join(self.instruction)
