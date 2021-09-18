from ..models import Mnemonic, DecodedInstruction

from .base_decoder import BaseDecoder


class ControlFlowInstructionDecoder(BaseDecoder):
    """
    Decoder that handles control flow instructions such as jump, jnz, etc.
    """
    def decode_instruction(self, byte_index, mnemonic: Mnemonic) -> DecodedInstruction:
        if mnemonic == Mnemonic.CALL:
            return self._decode_call(byte_index)
        elif mnemonic == Mnemonic.CALL_FLUSH:
            return self._decode_call_flush(byte_index)
        elif mnemonic == Mnemonic.JUMP:
            return self._decode_jump(byte_index)
        elif mnemonic == Mnemonic.JUMP_ZERO:
            return self._decode_jump_zero(byte_index)
        elif mnemonic == Mnemonic.JUMP_NOT_ZERO:
            return self._decode_jump_not_zero(byte_index)
        elif mnemonic == Mnemonic.RETURN_FAR:
            return self._decode_return_far(byte_index)
        elif mnemonic == Mnemonic.RETURN_NEAR:
            return self._decode_return_near(byte_index)

        raise Exception('Attemted to decode instruction {} with the wrong decoder.'.format(mnemonic))

    def _decode_call(self, byte_index) -> DecodedInstruction:
        pass

    def _decode_call_flush(self, byte_index) -> DecodedInstruction:
        pass

    def _decode_jump(self, byte_index) -> DecodedInstruction:
        pass

    def _decode_jump_zero(self, byte_index) -> DecodedInstruction:
        pass

    def _decode_jump_not_zero(self, byte_index) -> DecodedInstruction:
        pass

    def _decode_return_far(self, byte_index) -> DecodedInstruction:
        # here
        pass

    def _decode_return_near(self, byte_index) -> DecodedInstruction:
        # here
        pass

