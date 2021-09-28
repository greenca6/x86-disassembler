from src.disassembler import Disassembler

max_byte = 256

def test_all_possibilities_with_one_byte_should_not_fail():
    """
    Tests that a single byte given to the dissassembler shouldn't fail by exhausting all combinations
    """
    disassembler = Disassembler()
    for i in range(max_byte):
        disassembler.disassemble([i])


def test_all_possibilities_with_two_bytes_should_not_fail():
    disassembler = Disassembler()
    for i in range(max_byte):
        for j in range(max_byte):
            disassembler.disassemble([i, j])

