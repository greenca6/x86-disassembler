# About

## Project Structure

This project has two high level components: an instruction matcher, and a collection of instruction decoders. The overall disassembler calls these two components in order to disassemble the given binary.

### Instruction Matcher

The `InstructionMatcher` holds a large dictionary of instruction definitions. Each instruction definition holds information about the given mnemonic (add, sub, lea, etc), it's corresponding opcode(s), and any potential "complex" opcodes (opcodes that have an extension or two-byte opcode).

The `InstrutionMatcher` can tell you what instruction matches a given byte, or pair of bytes. It will return the mnemonic associated with the byte(s).

This is what allows the disassembler to know "how" to decode the next N number of bytes. It will use the mnemonic that the `InstructionMatcher` returns to call the correct `InstructionDecoder`

### Instruction Decoders

The `InstructionDecoder`, or series of decoders, actually takes an input array of bytes, and returns the fully decoded instruction.

There are 4 high level decoders, broken down in terms of their categorical operation. The arithmetic decoder handles operations such as add, sub, mul, etc. The control flow decoder will handle operations that break the linear flow of the program (jmp, jze, etc). The logical decoder will handle instructions dealing with logical or bitwise operations (sal, not, or, xor, etc). And finally the miscelaneous decoder handles all the instructions that aren't easily categorized under the previous three categories (mov, nop, lea, etc).

Categorizing the decoders in this way was done purely as a means to better organize the code and to detect bugs.

Finally a parent `BaseDecoder` was created to give common functionality to all of the categorical decoders. A lot of the logic behind reading and deciphering immediates, modr/m bits, and the like lives here.

## Lessons Learned

### About The Project Structure 

It's debatable whether splitting the disassembly into finding instruction "matches", followed by actually "decoding" the matched instruction was the best idea. In reality, if you have already read one or two bytes to determine what instruction that binary matches (add, sub, lea, jze, etc), then you're probably at least halfway there to decoding the entire instruction.

The benefit of splitting these two apart is that is logically separates the workflow into two classes/files, which has the impact of making the code more modular and easier to find bugs. However, this does mean that there is some overlap when it comes to reading bits.

### About Reading Bytes Via Pointer

Throughout the program, bytes are read simply by making index references to the "next" bit. The effect that this has is that reading more bits that complete an instruction are made by incrementing the pointer until completion. This is a shakey way to "move" across the byte array, because it requires a close attention to detail on making sure that this index pointer is always accurrate - which is tedious given that every instruction has a variable byte length.

The benefit of this approach however is that the byte array is always "stable" - ie no part of the program is ever writing to it.

An alternative approach would have been to model the byte array in a queue type of structure - where we can actually remove bytes off of the queue - directly indicating the "next" bit to be read (as well as the bits already read). The downside of this is that sometimes we need to "backtrack" - say if there was an invalid 5-byte instruction given to us where we now need to make that first byte `db 0x##`, then start reading again from the second byte. Writing to any type of data structure in this way can create instability.
