from ..models import Mnemonic, DecodedInstruction

from .base_decoder import BaseDecoder


class LogicalInstructionDecoder(BaseDecoder):
    """
    Decoder that handles logical or boolean operations such as or, xor, sal, etc.
    """
    def decode_instruction(self, byte_index, mnemonic: Mnemonic) -> DecodedInstruction:
        if mnemonic == Mnemonic.AND:
            return self._decode_and(byte_index)
        elif mnemonic == Mnemonic.COMPARE:
            return self._decode_compare(byte_index)
        elif mnemonic == Mnemonic.NEGATE:
            return self._decode_negate(byte_index)
        elif mnemonic == Mnemonic.NOT:
            return self._decode_not(byte_index)
        elif mnemonic == Mnemonic.OR:
            return self._decode_or(byte_index)
        elif mnemonic == Mnemonic.SHIFT_ARITHMETIC_LEFT:
            return self._decode_shift_arithmetic_left(byte_index)
        elif mnemonic == Mnemonic.SHIFT_LOGICAL_RIGHT:
            return self._decode_shift_arithmetic_right(byte_index)
        elif mnemonic == Mnemonic.SHIFT_LOGICAL_RIGHT:
            return self._decode_shift_logical_right(byte_index)
        elif mnemonic == Mnemonic.TEST:
            return self._decode_test(byte_index)
        elif mnemonic == Mnemonic.OR:
            return self._decode_exclusive_or(byte_index)

        raise Exception('Attemted to decode instruction {} with the wrong decoder.'.format(mnemonic))
    
    def _decode_and(self, byte_index) -> DecodedInstruction:
        pass

    def _decode_compare(self, byte_index) -> DecodedInstruction:
        pass

    def _decode_negate(self, byte_index) -> DecodedInstruction:
        pass

    def _decode_not(self, byte_index) -> DecodedInstruction:
        pass

    def _decode_or(self, byte_index) -> DecodedInstruction:
        # here
        pass

    def _decode_shift_arithmetic_left(self, byte_index) -> DecodedInstruction:
        pass

    def _decode_shift_arithmetic_right(self, byte_index) -> DecodedInstruction:
        pass

    def _decode_shift_logical_right(self, byte_index) -> DecodedInstruction:
        pass

    def _decode_test(self, byte_index) -> DecodedInstruction:
        pass

    def _decode_exclusive_or(self, byte_index) -> DecodedInstruction:
        pass
