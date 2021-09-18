from typing import List


class DecodedInstruction:
    def __init__(self, instruction: List[str], total_bytes: int) -> None:
        self.instruction = instruction
        self.total_bytes = total_bytes
