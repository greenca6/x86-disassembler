from ..models import Mnemonic, DecodedInstruction

from .base_decoder import BaseDecoder


class MiscInstructionDecoder(BaseDecoder):
    """
    Decocder that handles all other instructions that aren't handled by the other decoders.
    """
    def decode_instruction(self, byte_index, mnemonic: Mnemonic) -> DecodedInstruction:
        if mnemonic == Mnemonic.LOAD_EFFECTIVE_ADDRESS:
            return self._decode_load_effective_address(byte_index)
        elif mnemonic == Mnemonic.MOVE:
            return self._decode_move(byte_index)
        elif mnemonic == Mnemonic.MOVE_STRING:
            return self._decode_move_string(byte_index)
        elif mnemonic == Mnemonic.NO_OP:
            return self._decode_no_op(byte_index)
        elif mnemonic == Mnemonic.OUTPUT_TO_PORT:
            return self._decode_output_to_port(byte_index)
        elif mnemonic == Mnemonic.POP:
            return self._decode_pop(byte_index)
        elif mnemonic == Mnemonic.PUSH:
            return self._decode_push(byte_index)
        elif mnemonic == Mnemonic.REPNE_CMPSD:
            return self._decode_repne_cmpsd(byte_index)

        raise Exception('Attemted to decode instruction {} with the wrong decoder.'.format(mnemonic))

    def _decode_load_effective_address(self, byte_index) -> DecodedInstruction:
        pass

    def _decode_move(self, byte_index) -> DecodedInstruction:
        # here
        pass

    def _decode_move_string(self, byte_index) -> DecodedInstruction:
        pass

    def _decode_no_op(self, byte_index) -> DecodedInstruction:
        pass

    def _decode_output_to_port(self, byte_index) -> DecodedInstruction:
        pass

    def _decode_pop(self, byte_index) -> DecodedInstruction:
        # here
        pass

    def _decode_push(self, byte_index) -> DecodedInstruction:
        # here
        pass

    def _decode_repne_cmpsd(self, byte_index) -> DecodedInstruction:
        pass

