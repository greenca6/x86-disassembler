from abc import ABC, abstractmethod
from typing import List

from ..models import Mnemonic, DecodedInstruction

class BaseDecoder(ABC):
    def __init__(self, bytes: List[int]) -> None:
        self.bytes = bytes

    @abstractmethod
    def decode_instruction(self, byte_index, mnemonic: Mnemonic) -> DecodedInstruction:
        raise Exception('decode_instruction must be overridden by a subclass.')

    def get_modrm_bits(self, modrm_byte) -> int:
        """
        returns the MOD, REG and RM values from the MOD R/M byte
        """
        mod = (modrm_byte & 0xc0) >> 6
        reg = (modrm_byte & 0x38) >> 3
        rm = (modrm_byte & 0x07)

        return (mod, reg, rm)

    def get_next_n_bytes(self, byte_index: int, n: int) -> str:
        bytes = []
        for i in range (n):
            print(self.bytes[byte_index + i])
            bytes.append(self.bytes[byte_index + i])

        bytes.reverse()
        bytes = map(lambda b: '%02X' % b, bytes)
        bytes = ''.join(bytes)

        return '0x{}'.format(bytes)
